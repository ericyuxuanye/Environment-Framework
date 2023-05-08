from dataclasses import dataclass
import datetime

from src.core import model, car, track

@dataclass 
class ModelInfo:
    __slots__ = "name", "version"
    
    name: str
    version: str


@dataclass 
class ArenaInfo:
    __slots__ = "track_name", "setup_id"

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
    __slots__ = "model_info", "start_time"

    arena_info: ArenaInfo
    round_to_finish: int
    model_info: ModelInfo

    def __init__(self, arena_info:ArenaInfo, round_to_finish:int, model_info:ModelInfo):
        self.arena_info = arena_info
        self.round_to_finish = round_to_finish
        self.model_info = model_info


@dataclass 
class RaceDataset:
    __slots__ = "model_info", "start_time"

    race_config: RaceConfig
    start_time: datetime
    steps : list[CarStateAction]

    def __init__(self, race_config:RaceConfig):
        self.race_config = race_config

    

@dataclass 
class Race:
    __slots__ = "model_info", "start_time"

    data : RaceDataset

    def __init__(self, race_config:RaceConfig):
        self.data = RaceDataset(race_config)

    def run():
        print('start')

        print('finish')

    def save_data(folder: str):
        pass
