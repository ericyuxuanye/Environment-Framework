import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from src.core.track import *

class TrackTest(unittest.TestCase):
    
    def test_000_tt(self):
        print(TileType.Road)
        print(TileType.Road.name)
        print(TileType.Road.value)
        print(list(TileType))

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

    def test_100_tf(self):
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
   
    def test_200_cv(self):
        print('\n===\ntest_cv')
        tf = self.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        cv = CarView(track_field = tf, position = car.Point2D(4.89, 2.16), view_radius = 2)
        print('\ncar view:', cv, '(up =', cv.up, ', left =', cv.left, ')')
        print('field:', cv.field)
        print('field shape:', cv.field.shape)


    def test_201_cv(self):
        print('\n===\ntest_cv')
        tf = self.sample_track_field_0()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        cv = CarView(track_field = tf, position = car.Point2D(4.89, 2.16), view_radius = 3)
        print('\ncar view:', cv, '(up =', cv.up, ', left =', cv.left, ')')
        print('field:', cv.field)
        print('field shape:', cv.field.shape)

        print('\nrange-type', type(range(0,4)))
 
    def __sample_track_field_1(cls) :
        y_size = 20
        x_size = 30
        tf = TrackField(y_size, x_size)

        # inner Wall
        tf.fill_block(range(8, 12), range(8, 22), TileType.Wall.value, 0)

        # inner Shoulder         
        tf.fill_block(range(6, 8), range(6, 24), TileType.Shoulder.value, 0)
        tf.fill_block(range(12, 14), range(6, 24), TileType.Shoulder.value, 0)
        tf.fill_block(range(8, 12), range(6, 8), TileType.Shoulder.value, 0)
        tf.fill_block(range(8, 12), range(22, 24), TileType.Shoulder.value, 0)

        # Road
        tf.fill_block(range(4, 6), range(4, 26), TileType.Road.value, 32767)
        tf.fill_block(range(14, 16), range(4, 26), TileType.Road.value, 32767)
        tf.fill_block(range(6, 14), range(4, 6), TileType.Road.value, 32767)
        tf.fill_block(range(6, 14), range(24, 26), TileType.Road.value, 32767)

        # outer Shoulder
        tf.fill_block(range(2, 4), range(2, 28), TileType.Shoulder.value, 0)
        tf.fill_block(range(16, 18), range(2, 28), TileType.Shoulder.value, 0)
        tf.fill_block(range(4, 16), range(2, 4), TileType.Shoulder.value, 0)
        tf.fill_block(range(4, 16), range(26, 28), TileType.Shoulder.value, 0)

        # outer Wall
        tf.fill_block(range(0, 2), range(0, 30), TileType.Wall.value, 0)
        tf.fill_block(range(18, 20), range(0, 20), TileType.Wall.value, 0)
        tf.fill_block(range(2, 18), range(0, 2), TileType.Wall.value, 0)
        tf.fill_block(range(2, 18), range(28, 30), TileType.Wall.value, 0)

        return tf

    def __sample_track_field_2(cls) :
        y_size = 20
        x_size = 30
        tf = TrackField(y_size, x_size)

        tf.fill_block(range(0, 20), range(0, 30), TileType.Wall.value, 0)
        tf.fill_block(range(2, 18), range(2, 28), TileType.Shoulder.value, 0)
        tf.fill_block(range(4, 16), range(4, 26), TileType.Road.value, TrackMark.Init.value)     
        tf.fill_block(range(7, 13), range(11, 19), TileType.Shoulder.value, 0)
        tf.fill_block(range(9, 11), range(13, 17), TileType.Wall.value, 0)

        # start line
        tf.mark_line(mark=TrackMark.Start, line=MarkLine(range(4, 7), range(14, 15)))

        # finish line
        tf.mark_line(mark=TrackMark.Finish, line=MarkLine(range(4, 7), range(13, 14)))

        return tf
    
    def test_301_tf(self):
        print('\n===\ntest_301_tf')
        tf = self.__sample_track_field_1()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

    def test_302_tf(self):
        print('\n===\ntest_302_tf')
        tf = self.__sample_track_field_2()
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

    def test_303_tf(self):
        print('\n===\ntest_303_tf')
        tf = self.__sample_track_field_2()

        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

        tf.compute_track_distance()
        print('\n=============\ncompute_track_distance()')
        print('tf field:', tf.field)
        print('tf field shape:', tf.field.shape)

if __name__ == '__main__':
    unittest.main()

