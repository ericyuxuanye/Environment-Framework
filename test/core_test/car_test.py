import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.car import *

class CarTest(unittest.TestCase):

    def test_000_p2d(self):
        print('\n===\ntest_000_p2d()')
        point = Point2D()
        print(point)
        self.assertTrue(point.x == 0)
        self.assertTrue(point.y == 0)


    def test_001_p2d(self):
        print('\n===\ntest_001_p2d()')
        point = Point2D(x = 3, y = 5.25)
        print(point)
        self.assertTrue(point.x == 3)
        self.assertTrue(point.y == 5.25)


    def test_002_p2d(self):
        print('\n===\ntest_002_p2d()')
        point = Point2D(3, 5.25)
        print(point)
        self.assertTrue(point.x == 3)
        self.assertTrue(point.y == 5.25)


    def test_003_p2d(self):
        print('\n===\ntest_003_p2d()')
        point = Point2D(y = 5.25, x = 3)
        print(point)
        self.assertTrue(point.x == 3)
        self.assertTrue(point.y == 5.25)


    def test_100_rf(self):
        print('\n===\ntest_100_rf()')
        r_friction = RotationFriction()
        print(r_friction)
        self.assertTrue(r_friction.min_accel_start == 0)
        self.assertTrue(r_friction.friction == 0)
        self.assertTrue(r_friction.max_velocity == 0)


    def test_101_rf(self):
        print('\n===\ntest_101_rf()')
        r_friction = RotationFriction(friction = 1, max_velocity=10.25)
        print(r_friction)
        self.assertTrue(r_friction.min_accel_start == 0)
        self.assertTrue(r_friction.friction == 1)
        self.assertTrue(r_friction.max_velocity == 10.25)


    def test_102_rf(self):
        print('\n===\ntest_102_rf()')
        r_friction = RotationFriction(min_accel_start = 1, friction = 0.5, max_velocity = 50)
        print(r_friction)
        self.assertTrue(r_friction.min_accel_start == 1)
        self.assertTrue(r_friction.friction == 0.5)
        self.assertTrue(r_friction.max_velocity < 50.01)
        self.assertTrue(r_friction.max_velocity > 50 - .01)


    def test_200_sf(self):
        print('\n===\ntest_200_sf()')
        s_friction= SlideFriction()
        print(s_friction)
        self.assertTrue(s_friction.min_velocity_start == 0)
        self.assertTrue(s_friction.friction == 0)


    def test_201_sf(self):
        print('\n===\ntest_201_sf()')
        s_friction= SlideFriction(min_velocity_start = 30, friction = 5)
        print(s_friction)
        self.assertTrue(s_friction.min_velocity_start == 30)
        self.assertTrue(s_friction.friction == 5)


    def test_300_cf(self):
        print('\n===\ntest_300_cf()')
        car_config= CarConfig()
        print(car_config)
        self.assertTrue(car_config.rotation_friction.min_accel_start == 0)
        self.assertTrue(car_config.slide_friction.min_velocity_start == 0)


    def test_301_cf(self):
        print('\n===\ntest_301_cf()')
        r_friction = RotationFriction(min_accel_start = 1, friction = 0.5, max_velocity = 50)
        s_friction= SlideFriction(min_velocity_start = 30, friction = 5)
        car_config= CarConfig(rotation_friction = r_friction, slide_friction = s_friction)

        print(car_config)
        self.assertTrue(car_config.rotation_friction.min_accel_start == 1)
        self.assertTrue(car_config.slide_friction.min_velocity_start == 30)


    def test_400_cf(self):
        print('\n===\ntest_400_cf()')
        car_info = CarInfo()
        print(car_info)
        self.assertTrue(car_info.id == 0)
        self.assertTrue(car_info.team == '')
        self.assertTrue(car_info.city == '')
        self.assertTrue(car_info.state == '')
        self.assertTrue(car_info.region == '')


    def test_500_ci(self):
        print('\n===\ntest_500_ci')
        car_info = CarInfo(id = 2976, team = 'spartabots', city = 'sammamish', state = 'wa', region = 'us')
        print(car_info)
        self.assertTrue(car_info.id == 2976)
        self.assertTrue(car_info.team == 'spartabots')
        self.assertTrue(car_info.city == 'sammamish')
        self.assertTrue(car_info.state == 'wa')
        self.assertTrue(car_info.region == 'us')


    def test_600_cs(self):
        print('\n===\ntest_600_cs()')
        car_state = CarState()
        print(car_state)
        self.assertTrue(car_state.position.x == 0)
        self.assertTrue(car_state.position.y == 0)


    def test_601_cs(self):
        print('\n===\ntest_601_cs()')
        car_state = CarState(forward_velocity=25)
        print(car_state)
        self.assertTrue(car_state.position.x == 0)
        self.assertTrue(car_state.position.y == 0)
        self.assertTrue(car_state.forward_velocity == 25)

        car_state.forward_velocity += .2
        print(car_state)
        self.assertTrue(car_state.forward_velocity == 25.2)


    def test_602_cs(self):
        print('\n===\ntest_602_cs()')
        car_state = CarState(position = Point2D(1.5, 2), timestamp=14696, 
            forward_velocity=25, slide_velocity=20.53, heading=.23, trackDistance=124)
        print('\n')
        print(car_state)
        self.assertTrue(car_state.position.x == 1.5)
        self.assertTrue(car_state.position.y == 2)


if __name__ == '__main__':
    unittest.main()

