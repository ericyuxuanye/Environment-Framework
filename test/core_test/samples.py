import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.track import *
from src.core.arena import *
from src.core.car import *
from src.core.race import *


@dataclass 
class ModelSpecialNumber(model.IModelInference):

    def load(self, folder:str) -> bool:
        return True

    def get_action(self, car_state: CarState, car_view: CarView) -> Action:
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
        y_size = 5
        x_size = 8
        tf = TrackField(y_size, x_size)
        for x in range(x_size) :
            tf.field[0, x]['type'] = TileType.Wall.value
            tf.field[1, x]['type'] = TileType.Shoulder.value
            tf.field[2, x]['type'] = TileType.Road.value
            tf.field[2, x]['distance'] = x
            tf.field[3, x]['type'] = TileType.Shoulder.value
            tf.field[4, x]['type'] = TileType.Wall.value
        
        return tf

    @classmethod
    def sample_track_field_1(cls) -> TrackField:
        y_size = 20
        x_size = 30
        tf = TrackField(y_size, x_size)

        # inner Wall
        tf.fill_block(range(8, 12), range(8, 22), TileType.Wall.value, 0)

        # inner Shoulder         
        tf.fill_block(range(6, 8), range(6, 24), TileType.Shoulder.value, 0)
        tf.fill_block(range(12, 14), range(6, 24), TileType.Shoulder.value, 0)
        tf.fill_block(range(8, 12), range(6, 8), TileType.Shoulder.value, 0)
        tf.fill_block(range(8, 12), range(22, 24), TileType.Shoulder.value, 0)

        # Road
        tf.fill_block(range(4, 6), range(4, 26), TileType.Road.value, 32767)
        tf.fill_block(range(14, 16), range(4, 26), TileType.Road.value, 32767)
        tf.fill_block(range(6, 14), range(4, 6), TileType.Road.value, 32767)
        tf.fill_block(range(6, 14), range(24, 26), TileType.Road.value, 32767)

        # outer Shoulder
        tf.fill_block(range(2, 4), range(2, 28), TileType.Shoulder.value, 0)
        tf.fill_block(range(16, 18), range(2, 28), TileType.Shoulder.value, 0)
        tf.fill_block(range(4, 16), range(2, 4), TileType.Shoulder.value, 0)
        tf.fill_block(range(4, 16), range(26, 28), TileType.Shoulder.value, 0)

        # outer Wall
        tf.fill_block(range(0, 2), range(0, 30), TileType.Wall.value, 0)
        tf.fill_block(range(18, 20), range(0, 20), TileType.Wall.value, 0)
        tf.fill_block(range(2, 18), range(0, 2), TileType.Wall.value, 0)
        tf.fill_block(range(2, 18), range(28, 30), TileType.Wall.value, 0)

        return tf

    @classmethod
    def sample_track_field_2(cls, compute_distance:bool = False) -> TrackField:
        y_size = 20
        x_size = 30
        tf = TrackField(y_size, x_size)

        tf.fill_block(range(0, 20), range(0, 30), TileType.Wall.value, 0)
        tf.fill_block(range(2, 18), range(2, 28), TileType.Shoulder.value, 0)
        tf.fill_block(range(4, 16), range(4, 26), TileType.Road.value, TrackMark.Init.value)     
        tf.fill_block(range(7, 13), range(11, 19), TileType.Shoulder.value, 0)
        tf.fill_block(range(9, 11), range(13, 17), TileType.Wall.value, 0)

        # start line
        start_line = MarkLine(TrackMark.Start, range(4, 7), range(14, 15))

        # finish line
        tf.fill_block(range(3, 4), range(12, 15), TileType.Wall.value, 0)   # block top by wall
        finish_line = MarkLine(TrackMark.Finish, range(4, 7), range(13, 14))
        tf.fill_block(range(7, 8), range(12, 15), TileType.Wall.value, 0)   # block bottom by wall
        
        if compute_distance:
            tf.compute_track_distance(start_line, finish_line)

        return tf
    
    @classmethod
    def default_car_config(cls) -> CarConfig:

        return CarConfig(
            rotation_friction = RotationFriction(min_accel_start = 2, friction = 0.5),
            slide_friction = SlideFriction(min_velocity_start = 4, friction = 2),
            motion_profile = MotionProfile(max_acceleration = 5, max_velocity = 50, max_angular_velocity = math.pi/2))


    @classmethod
    def sample_arena_0(cls) -> Arena:

        tf = cls.sample_track_field_2(True)
        car_config = cls.default_car_config()

        return Arena(track_field = tf, view_radius = 2, time_interval = 100, car_config = car_config)


    @classmethod
    def sample_race_0(cls) -> Race:
        arena = cls.sample_arena_0()
        arena_info = ArenaInfo(track_name="sample_track_field_2", view_radius = arena.view_radius, car_config = arena.car_config)
        
        model = ModelSpecialNumber()
        model_info = ModelInfo(name='simplefixedrightturn', version='0.0.21')
        
        car_info = CarInfo(id = 1024, team = 'kirin')
        race_info = RaceInfo(
            arena_info = arena_info, 
            round_to_finish = 1, 
            model_info = model_info,
            car_info = car_info)

        start_state = CarState(position = Point2D(y = 5.5, x = 14.5))
        return Race(race_info = race_info, arena =arena, model = model, start_state = start_state)

