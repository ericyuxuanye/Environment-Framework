import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from core.src.track import *
from core.src.car import *
from core.src.race import *



class Model(model.IModelInference):

    def load(self, folder:str) -> bool:
        return True

    def get_action(self, car_state: CarState) -> Action:
        if car_state.position.x > 14 and car_state.position.x < 18 and car_state.position.y < 7:
            return Action(2, 0)
        elif car_state.position.x > 18 and car_state.position.y < 14:
            return Action(2, 1.2)
        elif car_state.position.x > 11 and car_state.position.y > 12: 
            return Action(2, 0)
        elif car_state.position.x < 11 and car_state.position.y < 14: 
            return Action(2, 1.75)     
        return Action(2, 0)


if __name__ == '__main__':
    model = Model()
    start_state = CarState(position = Point2D(y = 5.5, x = 14.5))

    action = model.get_action(start_state)
    print(action)