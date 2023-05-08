from dataclasses import dataclass
from datetime import datetime

from src.core import model, car, track

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
class CarStateAction:
    __slots__ = "car_state", "action"

    car_state:  car.CarState
    action:     car.Action



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
    steps : list[CarStateAction]

    def __init__(self, race_config:RaceConfig):
        self.race_config = race_config
        self.steps = []


@dataclass 
class Race:
    __slots__ = "data", "model"

    data : RaceDataset
    model : model.IModelInference 

    def __init__(self, race_config:RaceConfig, model: model.IModelInference):
        self.data = RaceDataset(race_config)
        self.model = model

    def run(self):
        print('start')
        self.data.start_time = datetime.now()

        print('finish')

    def save_data(folder: str):
        pass
