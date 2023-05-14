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



    def test_400_too_low_power(self):
        print('\n===\ntest_400_too_low_power')

        tf = Factory.sample_track_field_2(True)
        
        low_power_action = car.Action(1,0)
        print('low_power_action = ', low_power_action)

        start_state = car.CarState(position = car.Point2D(y = 5.5, x = 14.5))
        state_1 = tf.get_next_state(
            car_config=Factory.default_car_config(), 
            car_state=start_state, 
            action=low_power_action)
        print('state_1 = ', state_1)
        self.assertTrue(state_1.velocity_x == 0)
        self.assertTrue(state_1.velocity_y == 0)
        self.assertTrue(state_1.wheel_angle == 0)
        self.assertTrue(state_1.tile_distance == 0)
        self.assertTrue(state_1.timestamp == tf.track_info.time_interval)

if __name__ == '__main__':
    unittest.main()

