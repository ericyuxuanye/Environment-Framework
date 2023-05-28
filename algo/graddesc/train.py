import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import random
import math
import numpy as np
from collections import namedtuple, deque

from core.src import model
from core.src.race import *

from model import *

Transition = namedtuple("Transition", ("state", "reward"))
BATCH_SIZE = 10
GAMMA = 0.999

class ReplayMemory:
    def __init__(self, capacity):
        self.memory = deque([], maxlen=capacity)

    def push(self, *args):
        self.memory.append(Transition(*args))

    def sample(self, batch_size):
        return random.sample(self.memory, batch_size)

    def __len__(self):
        return len(self.memory)

class ModelTrain(model.IModelInference):
    def __init__(self, model:Model, race:Race):
        self.model = model
        self.race = race
        self.target = CarNet(INPUT_VECTOR_SIZE).to(device)
        self.target.training = True
        self.optimizer = optim.Adam(self.target.parameters(), lr=1e-4, amsgrad=True)
        

    def load(self, folder:str) -> bool:
        loaded = self.model.load(folder)
        self.target.load_state_dict(self.model.net.state_dict())
                
        return loaded
    

    def save(self, folder:str) -> bool:
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            torch.save(self.target.state_dict(), f=model_path)
            return True
        except:
            print(f"Failed to save model into {model_path}")
            return False
        
   
    def train(self, round_count:int) -> float:

        total_score:float = 0
        for round in range(round_count):

            self.race.run(debug=False)
            final_state = race.steps[-1].car_state

            reward = final_state.track_state.score
            print(f"round {round}: reward {reward}")
            reward_tensor = torch.tensor([reward+1], device=device)
            total_score += reward

            self.memory = ReplayMemory(len(race.steps))

            for step in race.steps:
                state = step.car_state
                state_tensor = self.model.state_tensor(state)
                self.memory.push(state_tensor, reward_tensor)

            for i in range(len(race.steps)):
                self.update_model()

            self.model.net.load_state_dict(self.target.state_dict())

        return total_score/round_count

    def update_model(self):

        transitions = self.memory.memory
        batch = Transition(*zip(*transitions))

        state_batch = torch.cat(batch.state)
        target_batch = self.target(state_batch)
        reward_batch = torch.cat(batch.reward)

        loss = F.smooth_l1_loss(target_batch, reward_batch.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.target.parameters(), 100)

        self.optimizer.step()

        

if __name__ == '__main__':

    model, race = create_model_race()

    model_train = ModelTrain(model, race)
    model_train.load(os.path.dirname(__file__))
    
    for epoch in range(20):
        average_score = model_train.train(50)
        print(f"epoch {epoch}: {average_score}")
        model_train.save(os.path.dirname(__file__))


