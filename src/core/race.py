from dataclasses import dataclass
from datetime import datetime

from src.core import model, car, track, arena

@dataclass 
class ModelInfo:

    name: str
    version: str

    def __init__(self, name:str , version:str):
        self.type = 'ModelInfo'
        self.name = name
        self.version = version

@dataclass 
class ArenaInfo:

    track_name: str
    view_radius: int
    car_config: car.CarConfig

    def __init__(self, track_name:str, view_radius: int, car_config:car.CarConfig):
        self.type = 'ArenaInfo'
        self.track_name = track_name
        self.view_radius = view_radius
        self.car_config = car_config


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
    arena_info: ArenaInfo
    round_to_finish: int
    model_info: ModelInfo
    car_info: car.CarInfo

    def __init__(self, 
                 name: str,
                 id: str,
                 arena_info: ArenaInfo, 
                 round_to_finish: int, 
                 model_info: ModelInfo, 
                 car_info: car.CarInfo):
        self.type = 'RaceInfo'
        self.name = name
        self.id = id  
        self.arena_info = arena_info
        self.round_to_finish = round_to_finish
        self.model_info = model_info
        self.car_info = car_info

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
    arena : arena.Arena
    model : model.IModelInference
    
    start_time: datetime
    start_state : car.CarState
    steps: list[ActionCarState]

    def __init__(self, 
            race_info:RaceInfo, 
            arena: arena.Arena, 
            model: model.IModelInference, 
            start_state: car.CarState):
        
        self.race_info = race_info
        self.arena = arena
        self.model = model
        self.start_state = start_state
        self.steps = []

    def run(self, debug:bool = False) -> RaceData:
    
        self.race_info.id = self.race_info.name + "_" + datetime.now().strftime("%Y%m%d_%H%M%S")

        current_state = self.start_state

        self.steps = []
        self.steps.append(ActionCarState(None, current_state))

        if debug:
            print('Race start at time', self.start_time)
            print(current_state)

        while ((current_state.timestamp < 1000 # let it start
               or (current_state.velocity_x != 0 or current_state.velocity_y != 0))
               and current_state.round_count < self.race_info.round_to_finish) :
            
            current_view = self.arena.get_car_view(current_state)
            action = self.model.get_action(current_state, current_view)
            next_state = self.arena.get_next_state(current_state, action, debug)
            self.steps.append(ActionCarState(action, next_state))
            
            if debug:
                print(action, next_state)

            current_state = next_state

        if debug:
            print('Race finished at time', datetime.now())
            print(current_state)

        return RaceData(self.race_info, self.steps)
        
