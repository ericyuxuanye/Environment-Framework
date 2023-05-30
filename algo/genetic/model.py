import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import numpy as np
import torch
from torch import nn
from torch.nn.parameter import Parameter

from core.src import model, car
from core.src.race import *
from core.test.samples import Factory


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# because we do not need gradients for GA
torch.set_grad_enabled(False)


INPUT_VECTOR_SIZE = 11
OUTPUT_VECTOR_SIZE = 2

DATA_FILE_NAME = "net_params.pt"

class Model(model.IModelInference):

    net:torch.nn.Sequential
    max_acceleration:float
    max_angular_velocity:float

    def __init__(self, max_acceleration:float = 1, max_angular_velocity:float = 1):
        self.net = self.create_net()
        self.max_acceleration = max_acceleration
        self.max_angular_velocity = max_angular_velocity

    def load(self, folder:str) -> bool:
        loaded = False
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            mode_data = torch.load(model_path)
            self.net.load_state_dict(mode_data)

            loaded = True
        except:
            print(f"Failed to load model from {model_path}")
            loaded = False
        return loaded

    def init_data(self) -> None:

        params = self.get_params()
        shapes = [param.shape for param in params]

        param_value: list[Parameter] = []
        for shape in shapes:
            # if fan in and fan out can be calculated (tensor is 2d) then using kaiming uniform initialisation
            # as per nn.Linear
            # otherwise use uniform initialisation between -0.05 and 0.05
            try:
                rand_tensor = nn.init.kaiming_uniform_(torch.empty(shape)).to(device)
            except ValueError:
                rand_tensor = nn.init.uniform_(torch.empty(shape), -0.2, 0.2).to(device)
            param_value.append((torch.nn.parameter.Parameter(rand_tensor)))

        self.set_params(param_value)

    
    """
        inference
    """

    def get_action(self, car_state: car.CarState) -> car.Action:
        
        input = np.empty((INPUT_VECTOR_SIZE), dtype=np.float32)
        input[0] = car_state.track_state.velocity_distance
        input[1] = car_state.track_state.velocity_angle_to_wheel
        input[2:11] = car_state.track_state.rays[0:9]

        tensor = torch.tensor(input).float().unsqueeze(0).to(device)
        output = self.net(tensor)
        action = torch.flatten(output).cpu().detach().numpy()
        return car.Action(self.max_acceleration*action[0], self.max_angular_velocity*action[1])



    @classmethod
    def create_net(cls):
        return nn.Sequential(
            nn.Linear(INPUT_VECTOR_SIZE, 32, bias=True),
            nn.Sigmoid(),
            nn.Linear(32, 16, bias=True),
            nn.Sigmoid(),
            nn.Linear(16, OUTPUT_VECTOR_SIZE, bias=True),
            nn.Tanh()
        ).to(device)


    """
        training
    """
    def get_params(self) -> list[Parameter]:

        params = []
        for layer in self.net:
            if hasattr(layer, "weight") and layer.weight != None:
                params.append(layer.weight)
            if hasattr(layer, "bias") and layer.bias != None:
                params.append(layer.bias)
        return params

    def set_params(self, params: list[Parameter]):
        i:int = 0
        for layerid, layer in enumerate(self.net):
            if hasattr(layer, "weight") and layer.weight != None:
                self.net[layerid].weight = params[i]
                i += 1
            if hasattr(layer, "bias") and layer.bias != None:
                self.net[layerid].bias = params[i]
                i += 1


def create_model_race() -> Race:
    race = Factory.sample_race_1()

    model = Model(race.race_info.car_config.motion_profile.max_acceleration, 
        race.race_info.car_config.motion_profile.max_angular_velocity)
    loaded = model.load(os.path.dirname(__file__))
    # print('Model load from data=', loaded)
    if not loaded:
        model.init_data()
    race.model = model

    race.race_info.model_info = ModelInfo(name='generic-hc', version='2023.5.18')
    race.race_info.round_to_finish = 2
    race.race_info.max_time_to_finish = 5000000

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

    for i in range(len(race.steps)):
        step = race.steps[i]
        if step.action != None:
            print(i
                  , f'action({step.action.forward_acceleration:.2f}, {step.action.angular_velocity:.2f})'
                  , step.car_state.track_state.tile_total_distance, step.car_state.track_state.score
                  , f'(x={step.car_state.position.x:.2f}, y={step.car_state.position.y:.2f})'
                  , f'(head={step.car_state.wheel_angle:.2f}, r={step.car_state.track_state.velocity_distance:.2f}, a={step.car_state.track_state.velocity_angle_to_wheel:.2f})'
                  )

