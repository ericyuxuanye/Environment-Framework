import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import numpy as np
import random
import torch
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim

from core.src import model, car
from core.src.race import *
from core.test.samples import Factory

INPUT_VECTOR_SIZE = 11
OUTPUT_VECTOR_SIZE = 9
device = "cpu"

TRAIN_EXPLOITION_RATE = 0.2


DATA_FILE_NAME = "policy_net.pt"

class DQN(nn.Module):
    def __init__(self, n_observations, n_actions):
        super(DQN, self).__init__()
        self.layer1 = nn.Linear(n_observations, 32)
        self.layer2 = nn.Linear(32, 32)
        self.layer3 = nn.Linear(32, 32)
        self.layer4 = nn.Linear(32, n_actions)

    def forward(self, input):
        output_1 = F.sigmoid(self.layer1(input))
        output_2 = F.sigmoid(self.layer2(output_1))
        output_3 = F.sigmoid(self.layer3(output_2))
        output_4 = self.layer4(output_3)
        return output_4
    
action_to_keys = [
    (0, 0, 0, 0),
    (0, 0, 1, 0),
    (1, 0, 1, 0),
    (0, 1, 1, 0),
    (1, 0, 0, 0),
    (0, 1, 0, 0),
    (0, 1, 0, 1),
    (0, 0, 0, 1),
    (1, 0, 0, 1),
]

class Model(model.IModelInference):

    def __init__(self, max_acceleration:float = 1, max_angular_velocity:float = 1, is_train:bool = False):
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity
        self.policy_net = DQN(INPUT_VECTOR_SIZE, OUTPUT_VECTOR_SIZE).to(device)
        self.is_train = is_train

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

    def init_data(self) -> None:
        self.init_weight(self.policy_net.layer1)
        self.init_bias(self.policy_net.layer1)
        self.init_weight(self.policy_net.layer2)
        self.init_bias(self.policy_net.layer2)
        self.init_weight(self.policy_net.layer3)
        self.init_bias(self.policy_net.layer3)


    @classmethod
    def init_weight(cls, layer:nn.Linear) -> None:
        layer.weight = torch.nn.parameter.Parameter(
            nn.init.kaiming_uniform_(torch.empty(layer.weight.shape)).to(device))
        
    @classmethod
    def init_bias(cls, layer:nn.Linear) -> None:
        layer.bias = torch.nn.parameter.Parameter(
            nn.init.uniform_(torch.empty(layer.bias.shape), -1, +1).to(device))

    @classmethod
    def state_tensor(cls, car_state: car.CarState) -> torch.tensor:
        
        input = np.empty((INPUT_VECTOR_SIZE), dtype=np.float32)
        input[0] = car_state.track_state.velocity_distance
        input[1] = car_state.track_state.velocity_angle_to_wheel
        input[2:11] = car_state.track_state.rays[0:9]
        input = torch.FloatTensor(input).reshape((1, 11)).to(device)

        return input

    @classmethod
    def action_tensor(cls, action: car.Action) -> torch.tensor:
        action_index = action_to_keys.index((action.angular_velocity == 1,
            action.angular_velocity == -1,
            action.forward_acceleration == 2,
            action.forward_acceleration == -1))
        action_tensor = torch.tensor([[action_index]], device=device)
        return action_tensor
    
    """
        inference
    """
    def get_action(self, car_state: car.CarState) -> car.Action:
        
        sample = random.random()
        if (self.is_train and sample < TRAIN_EXPLOITION_RATE
            or not self.is_train):
            input = self.state_tensor(car_state)
            net_output = self.policy_net(input)
            max = net_output.max(1)
            top = max[1]
            view = top.view(1, 1)
            action_index = view[0,0].int()
        else:
            action_index = random.randrange(3)  # only use action accel and turn, to enable move out init tile

        action_choice = action_to_keys[action_index]

        angular_velocity = 0
        if action_choice[0]:
            angular_velocity = 1
        if action_choice[1]:
            angular_velocity = -1
        
        forward_acceleration = 0
        if action_choice[2]:
            forward_acceleration = 2
        if action_choice[3]:
            forward_acceleration = -1

        return car.Action(forward_acceleration, angular_velocity)


def create_model_race() -> Race:
    race = Factory.sample_race_1()

    model = Model(race.race_info.car_config.motion_profile.max_acceleration, 
        race.race_info.car_config.motion_profile.max_angular_velocity)
    
    # normal value is 2, but q-learning only have option of 1,0,-1, need this be less than 1
    race.race_info.car_config.rotation_friction.min_accel_start = 0.5 

    loaded = model.load(os.path.dirname(__file__))
    print('Model load from data=', loaded)
    if not loaded:
        model.init_data()
     
    race.model = model
    race.race_info.model_info = ModelInfo(name='q_learning-hc', version='2023.5.22')
    race.race_info.round_to_finish = 1
    race.race_info.max_time_to_finish = 10000

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
