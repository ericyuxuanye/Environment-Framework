import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.track import *
from arena_sample import ArenaSample

class ArenaTest(unittest.TestCase):
    
    def test_100_arena(self):
        print('\n===\ntest_100_arena')

        arena = ArenaSample.sample_arena_0()
        print(arena)
        print('view_radius =', arena.view_radius)
        print('car_config =', arena.car_config)
        print('track_field =\n', arena.track_field.field)
        print('field.shape =', arena.track_field.field.shape)


        start_state = car.CarState(position = car.Point2D(y = 5.5, x = 14.5))
        print('start_state = ', start_state)
        self.assertTrue(start_state.trackDistance == 0)
        self.assertTrue(start_state.velocity_x == 0)
        self.assertTrue(start_state.velocity_y == 0)
        self.assertTrue(start_state.wheel_angle == 0)
        
        start_view = arena.get_car_view(start_state)
        print('start_view = ', start_view)

        print('car_config = ', arena.car_config)
    
        time_interval = 100 # 100 msec

        """
        low_power_action = car.Action(1,0)
        print('low_power_action = ', low_power_action)
        state_1 = arena.get_next_state(start_state, low_power_action, time_interval)
        print('state_1 = ', state_1)
        self.assertTrue(state_1.velocity_x == 0)
        self.assertTrue(state_1.velocity_y == 0)
        self.assertTrue(state_1.wheel_angle == 0)
        self.assertTrue(state_1.trackDistance=0 == 0)
        self.assertTrue(state_1.timestamp == time_interval)
        """


        startable_power_action = car.Action(2,0)
        print('startable_power_action = ', startable_power_action)
        state_2 = arena.get_next_state(start_state, startable_power_action, time_interval)
        print('state_2 = ', state_2)
        self.assertTrue(abs(state_2.velocity_x - 0.15) < 1e-5)
        self.assertTrue(state_2.velocity_y == 0)
        self.assertTrue(state_2.wheel_angle == 0)
        self.assertTrue(state_2.trackDistance == 0)
        self.assertTrue(state_2.timestamp == time_interval)
        self.assertTrue(state_2.position.x == start_state.position.x)
        self.assertTrue(state_2.position.y == start_state.position.y)

        state_3 = arena.get_next_state(state_2, startable_power_action, time_interval)
        print('state_3 = ', state_3)
        self.assertTrue(abs(state_3.velocity_x - 0.3) < 1e-5)
        self.assertTrue(state_3.velocity_y == 0)
        self.assertTrue(state_3.wheel_angle == 0)
        self.assertTrue(state_3.trackDistance == 0)
        self.assertTrue(state_3.timestamp - state_2.timestamp == time_interval)
        self.assertTrue(abs(state_3.position.x - start_state.position.x - 0.015) < 1e-5)
        self.assertTrue(state_3.position.y == start_state.position.y)

if __name__ == '__main__':
    unittest.main()

