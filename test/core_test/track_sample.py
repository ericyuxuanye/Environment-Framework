import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from src.core.track import *

class TrackSample:

    @classmethod
    def sample_track_field_0(cls) -> TrackField:
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

    @classmethod
    def sample_track_field_1(cls) -> TrackField:
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

    @classmethod
    def sample_track_field_2(cls) -> TrackField:
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
    
