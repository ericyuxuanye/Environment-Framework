
import unittest 
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.core.car import *

class CarTest(unittest.TestCase):

    def test_p2d0(self):
        point = Point2D()
        print('\n')
        print(point)
        self.assertTrue(point.x == 0)
        self.assertTrue(point.y == 0)


    def test_p2d1(self):
        point = Point2D(x = 3, y = 5.25)
        print('\n')
        print(point)
        self.assertTrue(point.x == 3)
        self.assertTrue(point.y == 5.25)


    def test_p2d2(self):
        point = Point2D(3, 5.25)
        print('\n')
        print(point)
        self.assertTrue(point.x == 3)
        self.assertTrue(point.y == 5.25)

    def test_p2d3(self):
        point = Point2D(y = 5.25, x = 3)
        print('\n')
        print(point)
        self.assertTrue(point.x == 3)
        self.assertTrue(point.y == 5.25)

    def test_rf0(self):
        r_friction = RotationFriction()
        print('\n')
        print(r_friction)
        self.assertTrue(r_friction.min_accel_start == 0)
        self.assertTrue(r_friction.friction == 0)
        self.assertTrue(r_friction.max_velocity == 0)


    def test_rf1(self):
        r_friction = RotationFriction(friction = 1, max_velocity=10.25)
        print('\n')
        print(r_friction)
        self.assertTrue(r_friction.min_accel_start == 0)
        self.assertTrue(r_friction.friction == 1)
        self.assertTrue(r_friction.max_velocity == 10.25)


    def test_rf(self):
        r_friction = RotationFriction(min_accel_start = 1, friction = 0.5, max_velocity = 50)
        print('\n')
        print(r_friction)
        self.assertTrue(r_friction.min_accel_start == 1)
        self.assertTrue(r_friction.friction == 0.5)
        self.assertTrue(r_friction.max_velocity < 50.01)
        self.assertTrue(r_friction.max_velocity > 50 - .01)


    def test_sf0(self):
        s_friction= SlideFriction()
        print('\n')
        print(s_friction)
        self.assertTrue(s_friction.min_velocity_start == 0)
        self.assertTrue(s_friction.friction == 0)

    def test_sf(self):
        s_friction= SlideFriction(min_velocity_start = 30, friction = 5)
        print('\n')
        print(s_friction)
        self.assertTrue(s_friction.min_velocity_start == 30)
        self.assertTrue(s_friction.friction == 5)


    def test_cf0(self):
        car_config= CarConfig()
        print('\n')
        print(car_config)
        self.assertTrue(car_config.rotation_friction.min_accel_start == 0)
        self.assertTrue(car_config.slide_friction.min_velocity_start == 0)


    def test_cf(self):
        r_friction = RotationFriction(min_accel_start = 1, friction = 0.5, max_velocity = 50)
        s_friction= SlideFriction(min_velocity_start = 30, friction = 5)
        car_config= CarConfig(rotation_friction = r_friction, slide_friction = s_friction)
        print('\n')
        print(car_config)
        self.assertTrue(car_config.rotation_friction.min_accel_start == 1)
        self.assertTrue(car_config.slide_friction.min_velocity_start == 30)


    def test_ci0(self):
        car_info = CarInfo()
        print('\n')
        print(car_info)
        self.assertTrue(car_info.id == 0)
        self.assertTrue(car_info.team == '')
        self.assertTrue(car_info.city == '')
        self.assertTrue(car_info.state == '')
        self.assertTrue(car_info.region == '')


    def test_ci(self):
        car_info = CarInfo(id = 2976, team = 'spartabots', city = 'sammamish', state = 'wa', region = 'us')
        print('\n')
        print(car_info)
        self.assertTrue(car_info.id == 2976)
        self.assertTrue(car_info.team == 'spartabots')
        self.assertTrue(car_info.city == 'sammamish')
        self.assertTrue(car_info.state == 'wa')
        self.assertTrue(car_info.region == 'us')


    def test_cs0(self):
        car_state = CarState()
        print('\n')
        print(car_state)
        self.assertTrue(car_state.location.x == 0)
        self.assertTrue(car_state.location.y == 0)


    def test_cs1(self):
        car_state = CarState(x_velocity=25)
        print('\n')
        print(car_state)
        self.assertTrue(car_state.location.x == 0)
        self.assertTrue(car_state.location.y == 0)
        self.assertTrue(car_state.x_velocity == 25)

        car_state.x_velocity += .2
        print(car_state)
        self.assertTrue(car_state.x_velocity == 25.2)


    def test_cs(self):
        car_state = CarState(location = Point2D(1.5, 2), timestamp=14696, x_velocity=25, y_velocity=20.53, angle=.23, trackDistance=124)
        print('\n')
        print(car_state)
        self.assertTrue(car_state.location.x == 1.5)
        self.assertTrue(car_state.location.y == 2)


if __name__ == '__main__':
    unittest.main()

