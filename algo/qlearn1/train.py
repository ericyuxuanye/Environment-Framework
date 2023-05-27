import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import random
import math
import numpy as np
from collections import namedtuple, deque

from core.src import model
from core.src.race import *
from core.test.samples import Factory
from model import *

Transition = namedtuple("Transition", ("state", "action", "reward"))
BATCH_SIZE = 256
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
        self.target_net = DQN(INPUT_VECTOR_SIZE, OUTPUT_VECTOR_SIZE).to(device)
        self.optimizer = optim.Adam(self.model.policy_net.parameters(), lr=0.1, amsgrad=True)
        self.memory = ReplayMemory(10000)

    def load(self, folder:str) -> bool:
        loaded = self.model.load(folder)
        self.target_net.load_state_dict(model.policy_net.state_dict())
                
        return loaded
    

    def save(self, folder:str) -> bool:
        try:
            model_path = os.path.join(folder, DATA_FILE_NAME)
            torch.save(self.model.policy_net.state_dict(), f=model_path)
            return True
        except:
            print(f"Failed to save model into {model_path}")
            return False
        
   
    def train(self, round_count:int) -> float:

        total_score:float = 0
        for round in range(round_count):
            self.race.run(debug=False)

            final_state = race.steps[-1].car_state
            #print(final_state)

            step_count = len(self.race.steps)
            if step_count > 0:
                step_0 = self.race.steps[0]
                current_state = step_0.car_state

            for i in range(1, step_count):
                step = self.race.steps[i]
                action = step.action
                next_state = step.car_state
             
                reward = final_state.track_state.score 

                current_state_tensor = self.model.state_tensor(current_state)
                action_tensor = self.model.action_tensor(action)
                reward_tensor = torch.tensor([reward], device=device)
                self.memory.push(current_state_tensor, action_tensor, reward_tensor)
                
                current_state = next_state

            to_run = int(final_state.track_state.score + step_count/10)
            total_score += final_state.track_state.score

            for i in range(to_run):
                self.update_model()

        return total_score/round_count

    def update_model(self):
        if len(self.memory) < BATCH_SIZE:
            return

        transitions = self.memory.sample(BATCH_SIZE)
        batch = Transition(*zip(*transitions))

        state_batch = torch.cat(batch.state)
        action_batch = torch.cat(batch.action)
        reward_batch = torch.cat(batch.reward)

        model_output = self.model.policy_net(state_batch)
        state_action_values = model_output.gather(1, action_batch)

        loss = F.smooth_l1_loss(state_action_values, reward_batch.unsqueeze(1))

        self.optimizer.zero_grad()
        loss.backward()
        torch.nn.utils.clip_grad_value_(self.model.policy_net.parameters(), 100)

        self.optimizer.step()

        

if __name__ == '__main__':

    model, race = create_model_race()
    model.is_train = True

    model_train = ModelTrain(model, race)
    model_train.load(os.path.dirname(__file__))
    
    for i in range(20):
        average_score = model_train.train(50)
        print(f"Training loop {i}: {average_score}")
        model_train.save(os.path.dirname(__file__))


