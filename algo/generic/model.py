import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import math
import numpy as np
import torch
from torch import nn
from torch.nn.parameter import Parameter

from core.src import model, car
from core.test.samples import Factory


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
# because we do not need gradients for GA
torch.set_grad_enabled(False)


INPUT_VECTOR_SIZE = 11
OUTPUT_VECTOR_SIZE = 2

DATA_FILE_NAME = "net_params.pt"

class Model(model.IModelInference):

    net:torch.nn.Sequential
    max_acceleration:float = 5
    max_angular_velocity:float = math.pi/2

    def __init__(self):
        self.net = self.create_net()

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


if __name__ == '__main__':
    
    model = Model()
    loaded = model.load(os.path.dirname(__file__))
    print('loaded=', loaded)

    race = Factory.sample_race_0()
    race.model = model
    start_state = race.race_info.start_state
    race.track_field.calc_track_state(start_state)

    action1 = model.get_action(start_state)
    print(action1)

    action2 = model.get_action(start_state)
    print(action2)

