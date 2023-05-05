
import numpy as np
from dataclasses import dataclass
from enum import Enum

from . import car

"""
Track system acts as physics engine.

A track field consists of equally sized tiles, with upper left corner as (0, 0).

A [500, 2000] track field has, upper right corner at (0, 1999),
lower left corner at (499, 0), and lower right corner at (499, 1999)
"""

# Use value as friction ratio => Shoulder surface friction is 3 * Road
class TileType(Enum):
    Road = 1
    Shoulder = 3
    Wall = 1024
    Block = 65535

# Special value for distance
class TrackMark(Enum):
    Start = 0                   # starting position
    End = 65535                 # end position, reach here means finished a round
    Init = 32767                # unknown value, not set 

@dataclass
class TrackField:
    __slots__ = ["field"]

    field: np.ndarray

    def __init__(self, row:int= 10, column:int = 10):
        self.field = np.zeros((row, column), dtype=np.dtype([('type', 'H'), ('distance', 'H')]))

    def fill_block(self, y_range: range, x_range: range , type: int, distance: int) :
        for y in y_range :
            for x in x_range :
                self.field[y, x]['type'] = type
                self.field[y, x]['distance'] = distance


@dataclass
class CarView:
    __slots__ = ["up", "left", "field"]

    up: int
    left: int
    field: np.ndarray

    def __init__(self, track_field: TrackField, position: car.Point2D, view_radius: int) -> None:
        """
        Creates a new CarView:
            track_field: the complete track field
            position : car position, center of car view
            view_radius: car visible distance in any direction, in meter.
        """
        field = track_field.field

        left = int(position.x - view_radius)
        if left < 0 :
            left = 0
        self.left = left

        right = int(position.x + view_radius + 1)
        if right > field.shape[1] :
            right = field.shape[1]
        right = int(right)

        up = int(position.y - view_radius)
        if up < 0 :
            up = 0
        self.up = up

        down = int(position.y + view_radius + 1)
        if down > field.shape[0] :
            down = field.shape[0]
        down = int(down)

        # print('[', up, ':', down, '][', left, ':', right, ']')
        self.field = field[up:down, :][:, left:right]


"""
TrackSystem acts as the physics engine.

It owns the TrackField, CarView radius. 

Usage:
    1. Construct TrackField, specify dimision, populate each tile type
    2. Specify Starting and Ending tiles
        Tiles between Starting and Ending tiles are properly edged on all side of the path
        Starting and Ending tiles can be same for round track. 
    3. Calculate distance for all road tiles. After this, the TrackSystem is initialized.



"""

# class TrackSystem:
    
    
    # def get_car_view(self, car_state: car.CarState) :
    #: CarView
    #    pass

    # def get_next_state(self, state: car.CarState, action: Action, interval: int):
    #    pass
