import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.track import *
from track_sample import TrackSample

class TrackTest(unittest.TestCase):
    
    def test_000_tt(self):
        print('\n===\ntest_000_tt')
        print(TileType.Road)
        print(TileType.Road.name)
        print(TileType.Road.value)
        print(list(TileType))

    def test_100_tf(self):
        print('\n===\ntest_100_tf')

        tf = TrackSample.sample_track_field_0()
        print(tf)
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
    
        tf = TrackSample.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        cv = CarView(track_field = tf, position = car.Point2D(4.89, 2.16), view_radius = 2)
        print('\ncar view:', cv, '(up =', cv.up, ', left =', cv.left, ')')
        print('field:', cv.field)
        print('field shape:', cv.field.shape)


    def test_201_cv(self):
        print('\n===\ntest_201_cv')
    
        tf = TrackSample.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        cv = CarView(track_field = tf, position = car.Point2D(4.89, 2.16), view_radius = 3)
        print('\ncar view:', cv, '(up =', cv.up, ', left =', cv.left, ')')
        print('field:', cv.field)
        print('field shape:', cv.field.shape)

        print('\nrange-type', type(range(0,4)))
  
    def test_301_tf(self):
        print('\n===\ntest_301_tf')

        tf = TrackSample.sample_track_field_1()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)


    def test_302_tf(self):
        print('\n===\ntest_302_tf')

        tf = TrackSample.sample_track_field_2()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)


    def test_303_tf(self):
        print('\n===\ntest_303_tf')

        tf = TrackSample.sample_track_field_2()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        tf.compute_track_distance()
        print('\n=============\ncompute_track_distance()')
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

if __name__ == '__main__':
    unittest.main()

