import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
import math
from src.core import car

import json
from src.core.fromjson import from_json

class JsonTest(unittest.TestCase):

    def default_car_config(cls) -> car.CarConfig:

        return car.CarConfig(
            rotation_friction = car.RotationFriction(min_accel_start = 2, friction = 0.5),
            slide_friction = car.SlideFriction(min_velocity_start = 4, friction = 2),
            motion_profile = car.MotionProfile(max_acceleration = 5, max_velocity = 50, max_angular_velocity = math.pi/2))


    def test_100_cc(self):
        print('\n===\ntest_100_cc()')

        cc_1= self.default_car_config()
        print('cc_1', cc_1)
        print('type(cc_1)', type(cc_1))
        cc_json = json.dumps(cc_1, default=lambda o: o.__dict__, indent=4)
        
        print('cc_json', cc_json)

        cc_2 = json.loads(cc_json)
        print('cc_2', cc_2)
        print('type(cc_2)', type(cc_2))

        cc_3 = from_json(cc_2)
        print('cc_3', cc_3)
        print('type(cc_3)', type(cc_3))

        print('cc_1 == cc_3', cc_1 == cc_3) 


    def test_101_cc(self):
        print('\n===\ntest_101_cc()')

        cc_1= self.default_car_config()
        with open('data\carconfig\cc_1.json', 'w') as f:
            json.dump(cc_1, f, default=lambda o: o.__dict__, indent=4)
        
        with open('data\carconfig\cc_1.json', 'r') as f:
            cc_2 = json.load(f)
        
        print('cc_2', cc_2)
        print('type(cc_2)', type(cc_2))

        cc_3 = from_json(cc_2)
        print('cc_3', cc_3)
        print('type(cc_3)', type(cc_3))

        print('cc_1 == cc_3', cc_1 == cc_3) 


if __name__ == '__main__':
    unittest.main()

