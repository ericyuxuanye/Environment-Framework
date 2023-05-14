import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.track import *
from samples import Factory

class TrackTest(unittest.TestCase):

    def test_000_tt(self):
        print('\n===\ntest_000_tt')
        print(TileType.Road)
        print(TileType.Road.name)
        print(TileType.Road.value)
        print(list(TileType))

    def test_100_tf(self):
        print('\n===\ntest_100_tf')

        tf = Factory.sample_track_field_0()
        #print(tf)
        print(tf.field)
        print('shape', tf.field.shape)

        print('\ndtype: ')
        print(tf.field.dtype)
    
        print('\nRow 0: ', tf.field[0])

        print('\nCel[0,0]:', tf.field[0, 0])
        print('type =', tf.field[0, 0]['type'])
        print('distance =', tf.field[0, 0]['distance'])

        tf.field[0, 0] = (3, 35)
        print('\nAfter1 Cel[0,0]:', tf.field[0, 0])
        print('type =', tf.field[0, 0]['type'])
        print('distance =', tf.field[0, 0]['distance'])

        tf.field[0, 0]['distance'] = 24
        print('\nAfter2 Cel[0,0]:', tf.field[0, 0])
        print('type =', tf.field[0, 0]['type'])
        print('distance =', tf.field[0, 0]['distance'])
   

    def test_200_cv(self):
        print('\n===\ntest_200_cv')
    
        tf = Factory.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)
        self.assertTrue(tf.field.shape[0] == 5)
        self.assertTrue(tf.field.shape[1] == 8)

        tv = tf.get_track_view(position = car.Point2D(4.89, 2.16))
        print('\n track view:', tv, '(up =', tv.up, ', left =', tv.left, ')')
        print('field:', tv.field)
        print('field shape:', tv.field.shape)
        self.assertTrue(tv.up == 0)
        self.assertTrue(tv.left == 2)
        self.assertTrue(tv.field.shape[0] == 5)
        self.assertTrue(tv.field.shape[1] == 5)

  
    def test_301_tf(self):
        print('\n===\ntest_301_tf')

        tf = Factory.sample_track_field_1()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        self.assertTrue(tf.field.shape[0] == 20)
        self.assertTrue(tf.field.shape[1] == 30)


    def test_302_tf(self):
        print('\n===\ntest_302_tf')

        tf = Factory.sample_track_field_2(False)
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)


    def test_303_tf(self):
        print('\n===\ntest_303_tf')

        tf = Factory.sample_track_field_2(True)
        self.assertTrue(tf.field.shape[0] == 20)
        self.assertTrue(tf.field.shape[1] == 30)

        print('\n=============\ncompute_track_distance()')
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)
        print('tf round_distance:', tf.track_info.round_distance)
        self.assertTrue(tf.track_info.round_distance == 29)

        print('track_info:', tf.track_info)

    def setUp(self):
        print('\n===\nArenaTest.setUp()')
    
        self.tf = Factory.sample_track_field_2(True)
        self.start_state = car.CarState(position = car.Point2D(y = 5.5, x = 14.5))

    def test_400_too_low_power(self):
        print('\n===\ntest_400_too_low_power')

        low_power_action = car.Action(1,0)
        print('low_power_action = ', low_power_action)

        state_1 = self.tf.get_next_state(
            car_config=Factory.default_car_config(), 
            car_state=self.start_state, 
            action=low_power_action)
        print('state_1 = ', state_1)
        self.assertTrue(state_1.velocity_x == 0)
        self.assertTrue(state_1.velocity_y == 0)
        self.assertTrue(state_1.wheel_angle == 0)
        self.assertTrue(state_1.tile_distance == 0)
        self.assertTrue(state_1.timestamp == self.tf.track_info.time_interval)


    def test_401_startable_power(self):
        print('\n===\ntest_401_startable_power()')

        startable_power_action = car.Action(2,0)
        print('startable_power_action = ', startable_power_action)
        state_2 = self.tf.get_next_state(
            car_config=Factory.default_car_config(), 
            car_state=self.start_state, 
            action = startable_power_action)
        print('state_2 = ', state_2)
        self.assertTrue(abs(state_2.velocity_x - 0.15) < 1e-5)
        self.assertTrue(state_2.velocity_y == 0)
        self.assertTrue(state_2.wheel_angle == 0)
        self.assertTrue(state_2.tile_distance == 0)
        self.assertTrue(state_2.timestamp == self.tf.track_info.time_interval)
        self.assertTrue(state_2.position.x == self.start_state.position.x)
        self.assertTrue(state_2.position.y == self.start_state.position.y)

        state_3 = self.tf.get_next_state(
            car_config=Factory.default_car_config(), 
            car_state=state_2, 
            action=startable_power_action)
        print('state_3 = ', state_3)
        self.assertTrue(abs(state_3.velocity_x - 0.3) < 1e-5)
        self.assertTrue(state_3.velocity_y == 0)
        self.assertTrue(state_3.wheel_angle == 0)
        self.assertTrue(state_3.tile_distance == 0)
        self.assertTrue(state_3.timestamp - state_2.timestamp ==  self.tf.track_info.time_interval)
        self.assertTrue(abs(state_3.position.x - self.start_state.position.x - 0.015) < 1e-5)
        self.assertTrue(state_3.position.y == self.start_state.position.y)

    def test_402_startable_fix_power(self):
        print('\n===\ntest_402_startable_fix_power()')

        startable_power_action = car.Action(2,0)

        current_state = self.start_state
        print(current_state)
        while current_state.timestamp < 3000:
            current_state = self.tf.get_next_state(
                car_config=Factory.default_car_config(), 
                car_state=current_state, 
                action=startable_power_action)
            print(current_state)

    def test_403_out_of_bound(self):
        print('\n===\ntest_403_out_of_bound()')

        startable_power_action = car.Action(2,0)

        current_state = self.start_state
        print(current_state)
        while current_state.timestamp < 5600:
            current_state = self.tf.get_next_state(
                car_config=Factory.default_car_config(), 
                car_state=current_state, 
                action=startable_power_action)
            print(current_state)


    def test_404_wall_step(self):
        print('\n===\ntest_404_wall_step()')

        startable_power_action = car.Action(2,0)

        state = car.CarState(
            timestamp=4200, 
            wheel_angle=0.0, 
            velocity_x=6.1, 
            velocity_y=0.0,
            position = car.Point2D(y = 5.5, x = 28.015))
        print('before: ', state, '\n')
        start_view = self.tf.get_track_view(state.position)
        print('\nstart_view = ', start_view, '\n')

        next = self.tf.get_next_state(
            car_config=Factory.default_car_config(), 
            car_state=state, 
            action=startable_power_action)
        print('\nafter: ', next, '\n')


    def test_405_right_turn(self):
        print('\n===\ntest_405_right_turn()')

        startable_power_action = car.Action(2,1)

        current_state = car.CarState(
            timestamp=1900, 
            wheel_angle=0.0, 
            velocity_x=2.5, 
            velocity_y=0.0,
            position = car.Point2D(y = 5.5, x = 17.065),
            tile_distance=3)
        print(current_state)

        while current_state.timestamp < 10000 and abs(current_state.velocity_x) > 0:
            current_state = self.tf.get_next_state(
                car_config=Factory.default_car_config(), 
                car_state=current_state, 
                action=startable_power_action)
            print(current_state)
        
        # stop on wall
        self.assertTrue(current_state.tile_type == 1024)

    def test_406_right_complete(self):
        print('\n===\ntest_406_right_complete()')

        startable_power_action = car.Action(2, 1.21)

        current_state = car.CarState(
            timestamp=1900, 
            wheel_angle=0.0, 
            velocity_x=2.5, 
            velocity_y=0.0,
            position = car.Point2D(y = 5.5, x = 17.065),
            tile_distance=3)
        print(current_state)

        while (current_state.timestamp < 10000 
               and abs(current_state.velocity_x) > 0
               and current_state.round_count < 1) :
            current_state = self.tf.get_next_state(
                car_config=Factory.default_car_config(), 
                car_state=current_state, 
                action=startable_power_action)
            print(current_state)

if __name__ == '__main__':
    unittest.main()

