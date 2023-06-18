import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import math
from src.track import *
from src.car import *
from src.race import *    

class ModelSpecialNumber(model.IModelInference):

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



class Factory:

    @classmethod
    def sample_track_field_0(cls) -> TrackField:

        track_info = TrackInfo(
            name='sample_track_field_0', 
            row=5, 
            column=8,
            time_interval = 1000)
    
        tf = TrackField(track_info)
        for x in range(track_info.column) :
            tf.field[0, x]['type'] = TileType.Wall.value
            tf.field[1, x]['type'] = TileType.Shoulder.value
            tf.field[2, x]['type'] = TileType.Road.value
            tf.field[2, x]['distance'] = x
            tf.field[3, x]['type'] = TileType.Shoulder.value
            tf.field[4, x]['type'] = TileType.Wall.value
        
        return tf

    @classmethod
    def sample_track_field_1(cls) -> TrackField:
        track_info = TrackInfo(
            name='sample_track_field_1', 
            row=20, 
            column=30, 
            time_interval = 1000)
        tf = TrackField(track_info)

        # inner Wall
        tf.fill_block(range(8, 12), range(8, 22), TileType.Wall.value)

        # inner Shoulder         
        tf.fill_block(range(6, 8), range(6, 24), TileType.Shoulder.value)
        tf.fill_block(range(12, 14), range(6, 24), TileType.Shoulder.value)
        tf.fill_block(range(8, 12), range(6, 8), TileType.Shoulder.value)
        tf.fill_block(range(8, 12), range(22, 24), TileType.Shoulder.value)

        # Road
        tf.fill_block(range(4, 6), range(4, 26), TileType.Road.value)
        tf.fill_block(range(14, 16), range(4, 26), TileType.Road.value)
        tf.fill_block(range(6, 14), range(4, 6), TileType.Road.value)
        tf.fill_block(range(6, 14), range(24, 26), TileType.Road.value)

        # outer Shoulder
        tf.fill_block(range(2, 4), range(2, 28), TileType.Shoulder.value)
        tf.fill_block(range(16, 18), range(2, 28), TileType.Shoulder.value)
        tf.fill_block(range(4, 16), range(2, 4), TileType.Shoulder.value)
        tf.fill_block(range(4, 16), range(26, 28), TileType.Shoulder.value)

        # outer Wall
        tf.fill_block(range(0, 2), range(0, 30), TileType.Wall.value)
        tf.fill_block(range(18, 20), range(0, 20), TileType.Wall.value)
        tf.fill_block(range(2, 18), range(0, 2), TileType.Wall.value)
        tf.fill_block(range(2, 18), range(28, 30), TileType.Wall.value)

        return tf

    @classmethod
    def sample_track_field_2(cls, compute_distance:bool = False, debug:bool = False) -> TrackField:
        track_info = TrackInfo(
            name='sample_track_field_2', 
            row=20, 
            column=30,
            start_line=MarkLine(4, 7, 14, 15),
            finish_line=MarkLine(4, 7, 13, 14),
            time_interval = 100)

        tf = TrackField(track_info)

        tf.fill_block(range(0, 20), range(0, 30), TileType.Wall.value)
        tf.fill_block(range(2, 18), range(2, 28), TileType.Shoulder.value)
        tf.fill_block(range(4, 16), range(4, 26), TileType.Road.value)     
        tf.fill_block(range(7, 13), range(11, 19), TileType.Shoulder.value)
        tf.fill_block(range(9, 11), range(13, 17), TileType.Wall.value)

   
        # hlock start and finish line by wall, allow only get to them from the road
        tf.fill_block(range(2, 4), range(12, 16), TileType.Wall.value)   # block top by wall
        tf.fill_block(range(7, 9), range(12, 16), TileType.Wall.value)   # block bottom by wall
        
        if compute_distance:
            tf.compute_tile_distance(debug)

        return tf
    
    @classmethod
    def default_car_config(cls) -> CarConfig:

        return CarConfig(
            rotation_friction = RotationFriction(min_accel_start = 2, friction = 0.5),
            slide_friction = SlideFriction(min_velocity_start = 4, friction = 2),
            motion_profile = MotionProfile(max_acceleration = 5, max_velocity = 50, max_angular_velocity = math.pi/2))


    @classmethod
    def sample_race_0(cls) -> Race:
        
        track_field = cls.sample_track_field_2(True)
 
        model = ModelSpecialNumber()
        model_info = ModelInfo(name='simplefixedrightturn', version='0.0.21')
        
        car_info = CarInfo(id = 1024, team = 'kirin')

        race_info = RaceInfo(
            name = 'TrackField2Radius2',
            id = 'NotStarted',
            round_to_finish = 1, 
            model_info = model_info,
            car_info = car_info,
            car_config= cls.default_car_config(),
            start_state = CarState(
                position = Point2D(y = 5.5, x = 14.5), 
                last_road_position = Point2D(y = 5.5, x = 14.5))
            )

        return Race(race_info = race_info, track_field = track_field, model = model)


    @classmethod
    def sample_race_1(cls) -> Race:
        
        track_field = cls.sample_track_field_2(True)

        model = ModelSpecialNumber()
        model_info = ModelInfo(name='simplefixedrightturn', version='0.0.21')
        car_info = CarInfo(id = 1024, team = 'kirin')

        race_info = RaceInfo(
            name = 'TrackField2Round3',
            id = 'NotStarted',
            track_info = track_field.track_info, 
            round_to_finish = 3,
            model_info = model_info, 
            car_info = car_info,
            car_config= cls.default_car_config(),
            start_state = CarState(
                position = Point2D(y = 5.5, x = 14.5), 
                last_road_position = Point2D(y = 5.5, x = 14.5))
            )

        return Race(race_info = race_info, track_field = track_field, model = model)