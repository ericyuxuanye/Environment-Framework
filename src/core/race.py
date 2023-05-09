from dataclasses import dataclass
from datetime import datetime

from src.core import model, car, track, arena

@dataclass 
class ModelInfo:
    __slots__ = "name", "version"
    
    name: str
    version: str


@dataclass 
class ArenaInfo:
    __slots__ = "track_name", "view_radius", "car_config"

    track_name: str
    view_radius: int
    car_config: car.CarConfig


@dataclass 
class CarActionState:
    __slots__ = "action", "car_state"

    action:     car.Action
    car_state:  car.CarState



@dataclass 
class RaceConfig:
    __slots__ = "arena_info", "round_to_finish", "model_info", "car_info"

    arena_info: ArenaInfo
    round_to_finish: int
    model_info: ModelInfo
    car_info: car.CarInfo

    def __init__(self, 
                 arena_info: ArenaInfo, 
                 round_to_finish: int, 
                 model_info: ModelInfo, 
                 car_info: car.CarInfo):
        self.arena_info = arena_info
        self.round_to_finish = round_to_finish
        self.model_info = model_info
        self.car_info = car_info


@dataclass 
class RaceDataset:
    __slots__ = "race_config", "start_time", "steps"

    race_config: RaceConfig
    start_time: datetime
    steps : list[CarActionState]

    def __init__(self, race_config:RaceConfig):
        self.race_config = race_config
        self.steps = []


@dataclass 
class Race:
    __slots__ = "data", "arena", "model", "start_state"

    data : RaceDataset
    arena : arena.Arena
    model : model.IModelInference
    start_state : car.CarState

    def __init__(self, 
            race_config:RaceConfig, 
            arena:arena.Arena, 
            model: model.IModelInference, 
            start_state: car.CarState):
        self.data = RaceDataset(race_config)
        self.arena = arena
        self.model = model
        self.start_state = start_state

    def run(self, debug:bool = False):

        self.data.start_time = datetime.now()
        current_state = self.start_state
        self.data.steps.append(CarActionState(None, current_state))
        if debug:
            print('Race start at time', self.data.start_time)
            print(current_state)

        while ((current_state.timestamp < 1000 # let it start
               or (current_state.velocity_x != 0 or current_state.velocity_y != 0))
               and current_state.round_count < self.data.race_config.round_to_finish) :
            
            current_view = self.arena.get_car_view(current_state)
            action = self.model.get_action(current_state, current_view)
            next_state = self.arena.get_next_state(current_state, action, debug)
            self.data.steps.append(CarActionState(action, next_state))
            
            if debug:
                print(action, next_state)

            current_state = next_state

        if debug:
            print('Race finished at time', datetime.now())
            print(current_state)

    def save_data(folder: str):
        pass
