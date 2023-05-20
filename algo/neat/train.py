import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import random
import math
import numpy as np
from itertools import count
import copy
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

POPULATION_SIZE = 10
TOP_SIZE = 2

CROSS_RATE = 0.65
CROSS_CHANCE = 0.6
MUTATION_FACTOR = 0.1
MUTATION_RATE = 0.15

POPULATION_FILE_NAME = "population.pt"
Parameters = list[Parameter]

class ModelTrain(model.IModelInference):

    def load(self, folder:str) -> bool:
        loaded = False
        try:
            config_path = os.path.join(folder, CONFIG_FILE_NAME)
            self.config = neat.Config(neat.DefaultGenome, 
                neat.DefaultReproduction, 
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation, 
                config_path)
            loaded = True
        except:
            print(f"Failed to load config from {config_path}")
            loaded = False
                
        return loaded
    

    def save(self, folder:str) -> bool:
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            with open(model_path, "wb") as f:
                pickle.dump(self.winner, f)
            return True
        except:
            print(f"Failed to save model into {model_path}")
            return False
        
   
    def train(self, generation_count:int = 100) :
        # Create the population, which is the top-level object for a NEAT run.
        population = neat.Population(self.config)

        # Add a stdout reporter to show progress in the terminal.
        population.add_reporter(neat.StdOutReporter(True))
        stats = neat.StatisticsReporter()
        population.add_reporter(stats)
        population.add_reporter(neat.Checkpointer(5))

        evaluator = neat.ParallelEvaluator(1, self.eval_model)
        self.winner = population.run(evaluator.evaluate, generation_count)

        print('\nBest genome:\n{!s}'.format(self.winner))
        print('Fitness:', self.winner.fitness)


    def eval_model(self, genome, config) -> float:

        race = Factory.sample_race_1()
        model = Model(
            race.race_info.car_config.motion_profile.max_acceleration, 
            race.race_info.car_config.motion_profile.max_angular_velocity)
        model.load_genome(genome, config)

        race.model = model
        race.race_info.model_info = ModelInfo(name='neat-hc', version='2023.5.20')
        race.race_info.round_to_finish = 50
        race.race_info.max_time_to_finish = 300000
        
        race.run()

        final_state = race.steps[-1].car_state
        # print(final_state)

        reward = (final_state.round_count*100
            + final_state.track_state.tile_total_distance 
            + final_state.track_state.last_road_tile_total_distance 
            - final_state.timestamp / 1000)
        return reward
    

if __name__ == '__main__':

    model_train = ModelTrain()
    loaded = model_train.load(os.path.dirname(__file__))
    print('loaded=', loaded)

    if not loaded:
        print('Fail to load NEAT config, exit')
        exit()

    model_train.train(30)
    model_train.save(os.path.dirname(__file__))


