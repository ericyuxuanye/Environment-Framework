import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.track import *
from samples import Factory

class ArenaTest(unittest.TestCase):
    def setUp(self):
        print('\n===\nArenaTest.setUp()')
    
        self.arena = Factory.sample_arena_0()
        print(self.arena)
        print('view_radius =', self.arena.view_radius)
        print('car_config =', self.arena.car_config)
        print('track_field =\n', self.arena.track_field.field)
        print('field.shape =', self.arena.track_field.field.shape)


        self.start_state = car.CarState(position = car.Point2D(y = 5.5, x = 14.5))
        print('start_state = ', self.start_state)
        self.assertTrue(self.start_state.track_distance == 0)
        self.assertTrue(self.start_state.velocity_x == 0)
        self.assertTrue(self.start_state.velocity_y == 0)
        self.assertTrue(self.start_state.wheel_angle == 0)


    def test_100_startview(self):
        print('\n===\ntest_100_startview()')

        print('car_config = ', self.arena.car_config)

        start_view = self.arena.get_track_view(self.start_state)
        print('start_view = ', start_view)


    def test_200_too_low_power(self):
        print('\n===\ntest_200_too_low_power()')
    
        low_power_action = car.Action(1,0)
        print('low_power_action = ', low_power_action)
        state_1 = self.arena.get_next_state(self.start_state, low_power_action)
        print('state_1 = ', state_1)
        self.assertTrue(state_1.velocity_x == 0)
        self.assertTrue(state_1.velocity_y == 0)
        self.assertTrue(state_1.wheel_angle == 0)
        self.assertTrue(state_1.track_distance == 0)
        self.assertTrue(state_1.timestamp == self.arena.time_interval)


    def test_201_startable_power(self):
        print('\n===\ntest_201_startable_power()')

        startable_power_action = car.Action(2,0)
        print('startable_power_action = ', startable_power_action)
        state_2 = self.arena.get_next_state(self.start_state, startable_power_action)
        print('state_2 = ', state_2)
        self.assertTrue(abs(state_2.velocity_x - 0.15) < 1e-5)
        self.assertTrue(state_2.velocity_y == 0)
        self.assertTrue(state_2.wheel_angle == 0)
        self.assertTrue(state_2.track_distance == 0)
        self.assertTrue(state_2.timestamp == self.arena.time_interval)
        self.assertTrue(state_2.position.x == self.start_state.position.x)
        self.assertTrue(state_2.position.y == self.start_state.position.y)

        state_3 = self.arena.get_next_state(state_2, startable_power_action)
        print('state_3 = ', state_3)
        self.assertTrue(abs(state_3.velocity_x - 0.3) < 1e-5)
        self.assertTrue(state_3.velocity_y == 0)
        self.assertTrue(state_3.wheel_angle == 0)
        self.assertTrue(state_3.track_distance == 0)
        self.assertTrue(state_3.timestamp - state_2.timestamp == self.arena.time_interval)
        self.assertTrue(abs(state_3.position.x - self.start_state.position.x - 0.015) < 1e-5)
        self.assertTrue(state_3.position.y == self.start_state.position.y)


    def test_202_startable_fix_power(self):
        print('\n===\ntest_202_startable_fix_power()')

        startable_power_action = car.Action(2,0)

        current_state = self.start_state
        print(current_state)
        while current_state.timestamp < 3000:
            current_state = self.arena.get_next_state(current_state, startable_power_action)
            print(current_state)


    def test_203_out_of_bound(self):
        print('\n===\ntest_203_out_of_bound()')

        startable_power_action = car.Action(2,0)

        current_state = self.start_state
        print(current_state)
        while current_state.timestamp < 5600:
            current_state = self.arena.get_next_state(current_state, startable_power_action)
            print(current_state)

    
    def test_204_wall_step(self):
        print('\n===\ntest_204_wall_step()')

        startable_power_action = car.Action(2,0)

        state = car.CarState(
            timestamp=4200, 
            wheel_angle=0.0, 
            velocity_x=6.1, 
            velocity_y=0.0,
            position = car.Point2D(y = 5.5, x = 28.015))
        print('before: ', state, '\n')
        start_view = self.arena.get_track_view(state)
        print('\nstart_view = ', start_view, '\n')

        next = self.arena.get_next_state(
            state, startable_power_action, debug=True)
        print('\nafter: ', next, '\n')
       

    def test_205_right_turn(self):
        print('\n===\ntest_205_right_turn()')

        startable_power_action = car.Action(2,1)

        current_state = car.CarState(
            timestamp=1900, 
            wheel_angle=0.0, 
            velocity_x=2.5, 
            velocity_y=0.0,
            position = car.Point2D(y = 5.5, x = 17.065),
            track_distance=3)
        print(current_state)

        while current_state.timestamp < 10000 and abs(current_state.velocity_x) > 0:
            current_state = self.arena.get_next_state(
                current_state, startable_power_action)
            print(current_state)
        # stop on wall

    def test_206_right_complete(self):
        print('\n===\ntest_206_right_complete()')

        startable_power_action = car.Action(2, 1.21)

        current_state = car.CarState(
            timestamp=1900, 
            wheel_angle=0.0, 
            velocity_x=2.5, 
            velocity_y=0.0,
            position = car.Point2D(y = 5.5, x = 17.065),
            track_distance=3)
        print(current_state)

        while (current_state.timestamp < 10000 
               and abs(current_state.velocity_x) > 0
               and current_state.round_count < 1) :
            current_state = self.arena.get_next_state(
                current_state, startable_power_action)
            print(current_state)

if __name__ == '__main__':
    unittest.main()

