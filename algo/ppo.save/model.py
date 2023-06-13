import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import math
import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from core.src import model, car
from core.src.race import *
from core.test.samples import Factory

INPUT_VECTOR_SIZE = 14


device = "cpu"

DATA_FILE_NAME = "policy_net.pt"

class RaceEnv(Env):
    def __init__(self, race:Race, model:model.IModelInference):
        self.race = race
        #self.action_space = spaces.Discrete(OUTPUT_VECTOR_SIZE)
        #self.observation_space = spaces.Box(low=-np.inf, high=np.inf, shape=(INPUT_VECTOR_SIZE,), dtype=np.float32)
        
    def reset(self):
        start_state = race.race_info.start_state
        self.race.track_field.calc_track_state(start_state)
        self.current_state = start_state
        return self.state_tensor(start_state)

    def step(self, action):
               
        next_state = self.race.track_field.get_next_state(self.race.race_info.car_config, self.current_state, action, debug=False)
     
        reward = next_state.track_state.tile_total_distance - self.current_state.track_state.tile_total_distance    
        done = (next_state.track_state.tile_type == track.TileType.Wall.value)

        self.current_state = next_state
        return self.state_tensor(next_state), reward, done, {}


    def render(self, mode='human'):
        pass

    def close(self):
        pass

    @classmethod
    def state_tensor(cls, car_state: car.CarState) -> torch.tensor:
        
        input = np.empty((INPUT_VECTOR_SIZE), dtype=np.float32)
        input[0] = car_state.position.x
        input[1] = car_state.position.y
        input[2] = car_state.wheel_angle
        input[3] = car_state.track_state.velocity_forward
        input[4] = car_state.track_state.velocity_right
        input[5:14] = car_state.track_state.rays[0:9]
        input = torch.FloatTensor(input).reshape((1, 14)).to(device)

        return input
    


class FeedForwardNN(nn.Module):
	def __init__(self, in_dim, out_dim):
		super(FeedForwardNN, self).__init__()

		self.layer1 = nn.Linear(in_dim, 64)
		self.layer2 = nn.Linear(64, 64)
		self.layer3 = nn.Linear(64, out_dim)

	def forward(self, x):
		activation1 = F.relu(self.layer1(x))
		activation2 = F.relu(self.layer2(activation1))
		output = self.layer3(activation2)

		return output


class Model(model.IModelInference):

    def __init__(self, max_acceleration:float = 1, max_angular_velocity:float = 1, is_train:bool = False):
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity
        self.policy_net = FeedForwardNN(INPUT_VECTOR_SIZE, OUTPUT_VECTOR_SIZE).to(device)

    def load(self, folder:str) -> bool:
        loaded = False
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            if os.path.exists(model_path):
                self.policy_net.load_state_dict(torch.load(model_path))
                loaded = True
        except:
            print(f"Failed to load q_learning model from {model_path}")
    
        return loaded

    @classmethod
    def state_tensor(cls, car_state: car.CarState) -> torch.tensor:
        
        input = np.empty((INPUT_VECTOR_SIZE), dtype=np.float32)
        input[0] = car_state.position.x
        input[1] = car_state.position.y
        input[2] = car_state.wheel_angle
        input[3] = car_state.track_state.velocity_forward
        input[4] = car_state.track_state.velocity_right
        input[5:14] = car_state.track_state.rays[0:9]
        input = torch.FloatTensor(input).reshape((1, 14)).to(device)

        return input

    def get_action(self, car_state: car.CarState) -> car.Action:

        input = self.state_tensor(car_state)
        action = self.policy_net(input).detach().numpy()

        car_acion = car.Action(action[0], action[1])
        # print('A:', acceleration_index-action_step, angular_velocity_index-action_step)
        return car_acion


def create_model_race() -> Race:
    race = Factory.sample_race_1()

    model = Model(race.race_info.car_config.motion_profile.max_acceleration, 
        race.race_info.car_config.motion_profile.max_angular_velocity)
    
    loaded = model.load(os.path.dirname(__file__))
    print('Model load from data=', loaded)
    #if not loaded:
    #    model.net.init_data() 

    race.model = model
    
    race.race_info.model_info = ModelInfo(name='graddesc-hc', version='2023.5.27')
    race.race_info.round_to_finish = 10
    race.race_info.max_time_to_finish = 100000

    return model, race

if __name__ == '__main__':

    model, race = create_model_race()

    start_state = race.race_info.start_state
    race.track_field.calc_track_state(start_state)
    print('start_state:\n', start_state)

    action = model.get_action(start_state)
    print('action at start:\n', action)

    race.run(debug=False)

    final_state = race.steps[-1].car_state
    print('race_info:\n', race.race_info)
    print('finish:\n', final_state)

    for i in range(len(race.steps)):
        step = race.steps[i]
        if step.action != None:
            print(i
                  , f'action({step.action.forward_acceleration:.2f}, {step.action.angular_velocity:.2f})'
                  , step.car_state.track_state.tile_total_distance, step.car_state.track_state.score
                  , f'(x={step.car_state.position.x:.2f}, y={step.car_state.position.y:.2f})'
                  , f'(head={step.car_state.wheel_angle:.2f}, v_forward={step.car_state.track_state.velocity_forward:.2f}, v_right={step.car_state.track_state.velocity_right:.2f})'
                  )
    
