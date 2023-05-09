import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.arena import *
from track_sample import TrackSample

class ArenaSample:

    @classmethod
    def default_car_config(cls) -> car.CarConfig:

        return car.CarConfig(
            rotation_friction = car.RotationFriction(min_accel_start = 2, friction = 0.5),
            slide_friction = car.SlideFriction(min_velocity_start = 4, friction = 2),
            motion_profile = car.MotionProfile(max_acceleration = 5, max_velocity = 50, max_angular_velocity = math.pi/2))


    @classmethod
    def sample_arena_0(cls) -> Arena:

        tf = TrackSample.sample_track_field_2()
        tf.compute_track_distance()
        car_config = __class__.default_car_config()

        return Arena(track_field = tf, view_radius = 2, time_interval = 100, car_config = car_config)


