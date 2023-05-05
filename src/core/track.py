
import numpy as np
from dataclasses import dataclass
from enum import Enum

from . import car

"""
Track system acts as the main physics engine.

A track field consists of equally sized tiles, with upper left corner as (0, 0).

A [500, 2000] track field has, upper right corner at (0, 1999),
lower left corner at (499, 0), and lower right corner at (499, 1999)
"""

# Use value as friction ratio => Shoulder surface friction is 3 * Road
class TileType(Enum):
    Road = 1
    Shoulder = 3
    Wall = 1024


class TrackField:
    __slots__ = ["field"]

    field: np.ndarray

    def __init__(self, row = 10, column = 10):
        self.field = np.zeros((row, column), dtype=np.dtype([('type', 'H'), ('distance', 'H')]))


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
class TrackSystem:
    def get_car_view(self, state: CarState) -> CarView:
"""
"""
        return subsection of TrackField visible to car at position of CarState.
"""

"""
        raise NotImplementedError

    def get_next_state(self, state: CarState, action: Action, interval: int):
"""
"""
        Returns the CarState using the Action after the time interval
        """
"""
        raise NotImplementedError


"""