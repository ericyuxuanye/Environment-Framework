import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import random
import math
import numpy as np
from itertools import count

from core.src import model, car
from core.test.samples import Factory
from model import *

import torch
from torch import nn
from torch.nn.parameter import Parameter
# because we do not need gradients for GA
torch.set_grad_enabled(False)

from torch.multiprocessing import Pool, set_start_method
try:
    set_start_method("spawn")
except RuntimeError:
    pass

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

POPULATION_SIZE = 200
TOP_SIZE = 10

CROSS_RATE = 0.45
CROSS_CHANCE = 0.6
MUTATION_FACTOR = 0.1
MUTATION_RATE = 0.15

POPULATION_FILE_NAME = "population.pt"
Parameters = list[Parameter]

class ModelTrain(model.IModelInference):

    model:Model
    model_loaded:bool = False
    population: list[Parameters]


    def __init__(self):
        self.model = Model()
        self.population = []


    def load(self, folder:str) -> bool:
        model_loaded = self.model.load(folder)

        loaded = False
        try:
            population_path = os.path.join(folder, POPULATION_FILE_NAME)
            self.population = torch.load(population_path)
            loaded = True
        except:
            print(f"Failed to load population from {population_path}")
            loaded = False

        if loaded:
            return loaded and model_loaded
                
        return False

    def init_population(self):
        params = self.model.get_params()
        shapes = [param.shape for param in params]
        self.population = []
        for _ in range(POPULATION_SIZE):
            entity = []
            for shape in shapes:
                # if fan in and fan out can be calculated (tensor is 2d) then using kaiming uniform initialisation
                # as per nn.Linear
                # otherwise use uniform initialisation between -0.5 and 0.5
                try:
                    rand_tensor = nn.init.kaiming_uniform_(torch.empty(shape)).to(device)
                except ValueError:
                    rand_tensor = nn.init.uniform_(torch.empty(shape), -0.2, 0.2).to(device)
                entity.append((torch.nn.parameter.Parameter(rand_tensor)))
            self.population.append(entity)
        
    def save(self, folder:str) -> bool:

        model_saved:bool = False
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            torch.save(self.model.net.state_dict(), model_path)
            model_saved = True
        except:
            print(f"Failed to save model into {model_path}")
            model_saved = False
        
        population_saved:bool = False
        try:
            population_path = os.path.join(folder, POPULATION_FILE_NAME)
            torch.save(self.population, population_path)
            population_saved = True
        except:
            print(f"Failed to save population into {population_path}")
            population_saved = False

        return model_saved and population_saved
    
    def train(self) :

        fitnesses = self.evaluate_population(self.population)
        print(f"fitnesses = {fitnesses}")
        n_fittest = [self.population[x] for x in np.argpartition(fitnesses, -10)[-10:]]
        
        fitnesses10 = self.evaluate_population(n_fittest)
        print(f"fitnesses10 = {fitnesses10}")

        """
        wheel = makeWheel(population, np.clip(fitnesses, 1, None))
        population = select(wheel, len(population) - 10)
        population.extend(n_fittest)
        last_10 = population[-10:]


        pop2 = list(population)
        for index in range(len(population) - 10):
            child = crossover(population[index], pop2)
            child = mutate(child)
            population[index] = child

        last_10_after = population[-10:]
        fitnesses10_2 = evaluate_population(last_10_after)
        print(f"fitnesses10 = {fitnesses10_2}")
        """
    
    def eval_model(self, params: list[Parameter]) -> float:
        model = Model()
        model.set_params(params)

        race = Factory.sample_race_0()
        race.model = model
        race.run()

        final_state = race.steps[-1].car_state
        # print(final_state)

        reward = (final_state.round_count*100
            + final_state.track_state.tile_total_distance 
            + final_state.track_state.last_road_tile_total_distance 
            - final_state.timestamp / 1000)
        return reward
    
    def evaluate_population(self, population: list[Parameters]) -> list[float]:
        fitnesses = np.array(list(map(self.eval_model, population)))
        avg_fitness = fitnesses.sum() / len(fitnesses)
        print(f"avg: {avg_fitness:6.2f}, fittest: {fitnesses.max():6.2f} at {fitnesses.argmax()}")
        return fitnesses




    def makeWheel(population, fitness: np.ndarray):
        wheel = []
        total = fitness.sum()
        top = 0
        for p, f in zip(population, fitness):
            f = f/total
            wheel.append((top, top+f, p))
            top += f
        return wheel


    def binSearch(wheel, num):
        mid = len(wheel)//2
        low, high, answer = wheel[mid]
        if low<=num<=high:
            return answer
        elif high < num:
            return binSearch(wheel[mid+1:], num)
        else:
            return binSearch(wheel[:mid], num)


    def select(wheel, N):
        answer = []
        while len(answer) < N:
            r = random.random()
            answer.append(binSearch(wheel, r))
        return answer

    def crossover(parent1: list[Parameter], pop: list[list[Parameter]]) -> list[Parameter]:
        """
        Crossover two individuals and produce a child.

        This is done by randomly splitting the weights and biases at each layer for the parents and then
        combining them to produce a child

        @params
            parent1 (Parameters): A parent that may potentially be crossed over
            pop (List[Parameters]): The population of solutions
        @returns
            Parameters: A child with attributes of both parents or the original parent1
        """
        if np.random.rand() < CROSS_RATE:
            index = np.random.randint(0, len(pop), size=1)[0]
            parent2 = pop[index]
            child = []
            mask = None

            for p1l, p2l in zip(parent1, parent2):
                # splitpoint = int(len(p1l) * split)
                # new_param = nn.parameter.Parameter(
                #     torch.cat([p1l[:splitpoint], p2l[splitpoint:]])
                # )
                # child.append(new_param)
                if len(p1l.shape) == 2:
                    mask = torch.bernoulli(torch.full((p1l.shape[0],), CROSS_CHANCE)).int()
                    tmp = mask.broadcast_to((p1l.shape[1], p1l.shape[0])).transpose(0, 1)
                else:
                    tmp = mask
                reverse_mask = torch.ones(p1l.shape).int() - tmp
                new_param = nn.parameter.Parameter(p1l * reverse_mask + p2l * tmp)
                child.append(new_param)

            return child
        else:
            return parent1


    def gen_mutate(shape: torch.Size) -> torch.Tensor:
        """
        Generate a tensor to use for random mutation of a parameter

        @params
            shape (torch.Size): The shape of the tensor to be created
        @returns
            torch.tensor: a random tensor
        """
        drop_rate = 1 - MUTATION_RATE
        dropout = nn.Dropout(drop_rate)(torch.ones(shape))
        randn = torch.randn(shape)
        result1 = dropout * randn 
        result = result1 * MUTATION_FACTOR
        return result


    def mutate(child: list[Parameter]) -> list[Parameter]:
        """
        Mutate a child

        @params
            child (Parameters): The original parameters
        @returns
            Parameters: The mutated child
        """
        for i in range(len(child)):
            for j in range(len(child[i])):
                gene = child[i][j]
                mutate = gen_mutate(child[i][j].shape)
                gene += mutate

        return child


if __name__ == '__main__':

    model_train = ModelTrain()
    loaded = model_train.load(os.path.dirname(__file__))
    print('loaded=', loaded)

    if not loaded:
        model_train.init_population()
        model_train.model.init_data()

    model_train.train()
