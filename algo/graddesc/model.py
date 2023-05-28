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


DATA_FILE_NAME = "target.pt"

class CarNet(nn.Module):
    def __init__(self, input_size:int):
        super().__init__()
        self.layer1 = nn.Linear(input_size, 32)
        self.layer2 = nn.Linear(32, 16)
        self.layer3 = nn.Linear(16, 16)
        self.layer4 = nn.Linear(16, 1)
        self.training = False


    def forward(self, input):
        layer1_output = self.layer1(input)
        output_1 = F.sigmoid(layer1_output)
        layer2_output = self.layer2(output_1)
        output_2 = F.sigmoid(layer2_output)
        layer3_output = self.layer3(output_2)
        self.action_output = F.tanh(layer3_output)
        self.layer4(self.action_output)
        return self.layer4(self.action_output) 

    def init_data(self) -> None:
        self.init_weight(self.layer1)
        self.init_bias(self.layer1)
        self.init_weight(self.layer2)
        self.init_bias(self.layer2)
        self.init_weight(self.layer3)
        self.init_bias(self.layer3)
        self.init_weight(self.layer4)
        self.init_bias(self.layer4)

    @classmethod
    def init_weight(cls, layer:nn.Linear) -> None:
        layer.weight = torch.nn.parameter.Parameter(
            nn.init.kaiming_uniform_(torch.empty(layer.weight.shape)).to(device))
        
    @classmethod
    def init_bias(cls, layer:nn.Linear) -> None:
        layer.bias = torch.nn.parameter.Parameter(
            nn.init.uniform_(torch.empty(layer.bias.shape), -.1, +.1).to(device))
        


class Model(model.IModelInference):

    def __init__(self, max_acceleration:float = 1, max_angular_velocity:float = 1):
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity
        self.net = CarNet(INPUT_VECTOR_SIZE).to(device)

    def load(self, folder:str) -> bool:
        loaded = False
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            if os.path.exists(model_path):
                self.net.load_state_dict(torch.load(model_path))
                loaded = True
        except:
            print(f"Failed to load q_learning model from {model_path}")
    
        return loaded

    @classmethod
    def state_tensor(cls, car_state: car.CarState) -> torch.tensor:
        
        input = np.empty((INPUT_VECTOR_SIZE), dtype=np.float32)
        input[0] = car_state.track_state.velocity_distance
        input[1] = car_state.track_state.velocity_angle_to_wheel
        input[2:11] = car_state.track_state.rays[0:9]
        input = torch.FloatTensor(input).reshape((1, 11)).to(device)

        return input

    
    """
        inference
    """
    def get_action(self, car_state: car.CarState) -> car.Action:
  
        input = self.state_tensor(car_state)
        self.net(input)
        action_output = self.net.action_output
        action_vector = torch.flatten(action_output).cpu().detach().numpy()

        car_acion = car.Action(self.max_acceleration*action_vector[0], self.max_angular_velocity*action_vector[1])
        return car_acion


def create_model_race() -> Race:
    race = Factory.sample_race_1()

    model = Model(race.race_info.car_config.motion_profile.max_acceleration, 
        race.race_info.car_config.motion_profile.max_angular_velocity)
    
    loaded = model.load(os.path.dirname(__file__))
    print('Model load from data=', loaded)
    if not loaded:
        model.net.init_data() 

    race.model = model
    
    race.race_info.model_info = ModelInfo(name='graddesc-hc', version='2023.5.27')
    race.race_info.round_to_finish = 1
    race.race_info.max_time_to_finish = 300000

    return model, race

if __name__ == '__main__':

    model, race = create_model_race()

    start_state = race.race_info.start_state
    race.track_field.calc_track_state(start_state)
    print('start_state:\n', start_state)

    action = model.get_action(start_state)
    print('action at start:\n', action)

    race.run(debug=True)

    final_state = race.steps[-1].car_state
    print('race_info:\n', race.race_info)
    print('finish:\n', final_state)
