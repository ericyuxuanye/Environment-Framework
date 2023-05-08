import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core import race, car
from arena_sample import ArenaSample
from model_sample import *


class RaceSample:

    @classmethod
    def sample_race_0(cls) -> race.Race:
        arena = ArenaSample.sample_arena_0()
        arena_info = race.ArenaInfo(track_name="sample_track_field_2", view_radius = arena.view_radius, car_config = arena.car_config)
        
        model = ModelForwardRight()
        model_info = race.ModelInfo(name='simplefixedrightturn', version='0.0.21')
        
        car_info = car.CarInfo(id = 1024, team = 'kirin')
        race_config = race.RaceConfig(
            arena_info = arena_info, 
            round_to_finish = 1, 
            model_info = model_info,
            car_info = car_info)

        return race.Race(race_config = race_config, model = model)


