from dataclasses import dataclass
from datetime import datetime

from . import model, car, track

@dataclass 
class ModelInfo:

    name: str
    version: str

    def __init__(self, name:str , version:str):
        self.type = 'ModelInfo'
        self.name = name
        self.version = version


@dataclass 
class ActionCarState:

    action:     car.Action
    car_state:  car.CarState

    def __init__(self, action:car.Action, car_state:car.CarState):
        self.type = 'ActionCarState'
        self.action = action
        self.car_state = car_state


@dataclass 
class RaceInfo:

    id: str 
    name: str
    track_info: track.TrackInfo
    round_to_finish: int
    model_info: ModelInfo
    car_info: car.CarInfo
    car_config : car.CarConfig
    start_state : car.CarState

    def __init__(self, 
                 name: str,
                 id: str,
                 track_info: track.TrackInfo, 
                 round_to_finish: int, 
                 model_info: ModelInfo, 
                 car_info: car.CarInfo,
                 car_config : car.CarConfig,
                 start_state : car.CarState):

        self.type = 'RaceInfo'
        self.name = name
        self.id = id  
        self.track_info = track_info
        self.round_to_finish = round_to_finish
        self.model_info = model_info
        self.car_info = car_info
        self.car_config = car_config
        self.start_state = start_state


@dataclass
class RaceData:
    
    race_info:RaceInfo
    steps: list[ActionCarState]

    def __init__(self, race_info:RaceInfo, steps: list[ActionCarState]):
        self.race_info = race_info
        self.steps = steps

@dataclass 
class Race:

    race_info : RaceInfo
    track_field : track.TrackField
    model : model.IModelInference

    steps: list[ActionCarState]

    def __init__(self, 
            race_info: RaceInfo, 
            track_field: track.TrackField, 
            model: model.IModelInference):
        
        self.race_info = race_info
        self.track_field = track_field
        self.model = model
        self.steps = []

    def run(self, debug:bool = False) -> RaceData:
    
        start_time = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.race_info.id = self.race_info.name + "_" + start_time

        current_state = self.race_info.start_state
        self.track_field.calc_track_state(current_state)

        self.steps = []
        self.steps.append(ActionCarState(None, current_state))

        if debug:
            print('Race start at time', start_time)
            print(current_state)

        while ((current_state.timestamp < 1000 # let it start
               or (current_state.velocity_x != 0 or current_state.velocity_y != 0))
               and current_state.round_count < self.race_info.round_to_finish) :
            
            action = self.model.get_action(current_state)
            next_state = self.track_field.get_next_state(self.race_info.car_config, current_state, action, debug)
            self.steps.append(ActionCarState(action, next_state))
            
            if debug:
                print(action, next_state)

            current_state = next_state

        if debug:
            print('Race finished at time', datetime.now())
            print(current_state)

        return RaceData(self.race_info, self.steps)
        
