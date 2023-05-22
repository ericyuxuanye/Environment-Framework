import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import pickle
import neat
import numpy as np

from core.src import model, car
from core.src.race import *
from core.test.samples import Factory

INPUT_VECTOR_SIZE = 11
OUTPUT_VECTOR_SIZE = 2

DATA_FILE_NAME = "neat_genome"
CONFIG_FILE_NAME = "config-feedforward"

class Model(model.IModelInference):

    def __init__(self, max_acceleration:float = 1, max_angular_velocity:float = 1):
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity

    def load(self, folder:str) -> bool:
        loaded = False
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            with open(model_path, "rb") as f:
                winner = pickle.load(f)
            
            config_path = os.path.join(folder, CONFIG_FILE_NAME)
            config = neat.Config(neat.DefaultGenome, 
                neat.DefaultReproduction, 
                neat.DefaultSpeciesSet,
                neat.DefaultStagnation, 
                config_path)

            self.net = neat.nn.FeedForwardNetwork.create(winner, config)
            loaded = True
        except:
            print(f"Failed to load NEAT model from {folder}")
            loaded = False
    
        return loaded

    def load_genome(self, genome, config):
        self.net = neat.nn.FeedForwardNetwork.create(genome, config)

    """
        inference
    """
    def get_action(self, car_state: car.CarState) -> car.Action:
        
        input = np.empty((INPUT_VECTOR_SIZE), dtype=np.float32)
        input[0] = car_state.track_state.velocity_distance
        input[1] = car_state.track_state.velocity_angle_to_wheel
        input[2:11] = car_state.track_state.rays[0:9]

        output = self.net.activate(input)
        return car.Action(self.max_acceleration*output[0], self.max_angular_velocity*output[1])


def create_model_race() -> Race:
    race = Factory.sample_race_1()

    model = Model(race.race_info.car_config.motion_profile.max_acceleration, 
        race.race_info.car_config.motion_profile.max_angular_velocity)
    loaded = model.load(os.path.dirname(__file__))
    if not loaded:
        print('Fail to load model, exit')
        exit()
    # print('Model load from data=', loaded)
    race.model = model
    race.race_info.model_info = ModelInfo(name='neat-hc', version='2023.5.20')
    race.race_info.round_to_finish = 50
    race.race_info.max_time_to_finish = 250000

    return model, race

if __name__ == '__main__':

    model, race = create_model_race()

    start_state = race.race_info.start_state
    race.track_field.calc_track_state(start_state)
    print('start_state:\n', start_state)

    action = model.get_action(start_state)
    print('action st start:\n', action)

    race.run(debug=False)

    final_state = race.steps[-1].car_state
    print('race_info:\n', race.race_info)
    print('finish:\n', final_state)
