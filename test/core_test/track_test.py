import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.track import *

class TrackTest(unittest.TestCase):
    
    """
    def test_tt(self):
        print(TileType.Road)
        print(TileType.Road.name)
        print(TileType.Road.value)
        print(list(TileType))

    """

    def sample_track_field_0(self) :
        y_size = 5
        x_size = 8
        tf = TrackField(y_size, x_size)
        for x in range(x_size) :
            tf.field[0, x]['type'] = TileType.Wall.value
            tf.field[1, x]['type'] = TileType.Shoulder.value
            tf.field[2, x]['type'] = TileType.Road.value
            tf.field[2, x]['distance'] = x
            tf.field[3, x]['type'] = TileType.Shoulder.value
            tf.field[4, x]['type'] = TileType.Wall.value
        
        return tf

    def test_tf(self):
        tf = self.sample_track_field_0()
        print('\n===\ntest_tf()')
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


    def test_cv0(self):
        print('\n===\ntest_cv0')
        tf = self.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        cv = CarView(track_field = tf, position = car.Point2D(4.89, 2.16), view_radius = 2)
        print('\ncar view:', cv, '(up =', cv.up, ', left =', cv.left, ')')
        print('field:', cv.field)
        print('field shape:', cv.field.shape)


    def test_cv1(self):
        print('\n===\ntest_cv1')
        tf = self.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        cv = CarView(track_field = tf, position = car.Point2D(4.89, 2.16), view_radius = 3)
        print('\ncar view:', cv, '(up =', cv.up, ', left =', cv.left, ')')
        print('field:', cv.field)
        print('field shape:', cv.field.shape)

if __name__ == '__main__':
    unittest.main()

