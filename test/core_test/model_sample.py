import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from dataclasses import dataclass
from src.core import model, car, track

@dataclass 
class ModelSpecialNumber(model.IModelInference):

    def load(self, folder:str) -> bool:
        return True

    def get_action(self, car_state: car.CarState, car_view: track.CarView) -> car.Action:
        if car_state.position.x > 14 and car_state.position.x < 18 and car_state.position.y < 7:
            return car.Action(2, 0)
        elif car_state.position.x > 18 and car_state.position.y < 14:
            return car.Action(2, 1.2)
        elif car_state.position.x > 11 and car_state.position.y > 12: 
            return car.Action(2, 0)
        elif car_state.position.x < 11 and car_state.position.y < 14: 
            return car.Action(2, 1.75)     
        return car.Action(2, 0)

    





