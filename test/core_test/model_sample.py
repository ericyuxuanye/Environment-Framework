import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core import model, car, track

class ModelForwardRight(model.IModelInference):
    def load(self, folder:str) -> bool:
        return True

    def get_action(self, car_state: car.CarState, car_view: track.CarView) -> car.Action:
        return car.Action(2, 1.2)
    





