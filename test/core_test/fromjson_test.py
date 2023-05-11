import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
import math
from src.core import car

import json
from src.core.fromjson import from_json

class JsonTest(unittest.TestCase):

    def test_100_cc(self):
        print('\n===\ntest_302_cf()')
        rf = car.RotationFriction(min_accel_start = 1, friction = 0.5)
        sf = car.SlideFriction(min_velocity_start = 30, friction = 5)
        mp = car.MotionProfile(max_velocity = 38.9, max_angular_velocity = math.pi, max_acceleration = 3)
       
        cc_1= car.CarConfig(motion_profile = mp, rotation_friction = rf, slide_friction = sf)
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



if __name__ == '__main__':
    unittest.main()

