
import numpy as np
from dataclasses import dataclass
from car import CarState
from model import Action

"""
This is the characteristics of the track. This file acts as the main physics engine.

A track field consists of equally sized tiles, with upper left corner as (0, 0).

A [500, 2000] track field has, upper right corner at (0, 1999),
lower left corner at (499, 0), and lower right corner at (499, 1999)
"""


FieldTile = np.dtype(
    [("type_id", np.uint8), ("is_center", np.bool_), ("distance", np.float64)]
)

Point = tuple[int, int]


class TrackField:
    __slots__ = ["field"]
    field: np.ndarray

    def __init__(self) -> None:
        self.field = np.zeros((500, 2000), dtype=FieldTile)


class CarView:
    __slots__ = ["upper_left", "field"]
    upper_left: Point
    field: np.ndarray

    def __init__(self, track_field: TrackField, x: int, y: int, view_distance: int) -> None:
        """
        Creates a new CarView

        Parameters:
            field: the TrackField of the car
            x: x coordinate of the car (center of returned view)
            y: y coordinate of the car (center of returned view)
            view_distance: distance that car can see in one direction from the center.
        """
        self.upper_left = (x - view_distance, y - view_distance)
        self.field = track_field.field[
            x - view_distance : x + view_distance + 1,
            y - view_distance : y + view_distance + 1,
        ]


class TrackSystem:
    def get_car_view(self, state: CarState) -> CarView:
        """
        return subsection of TrackField visible to car at position of CarState.
        """
        raise NotImplementedError

    def get_next_state(self, state: CarState, action: Action, interval: int):
        """
        Returns the CarState using the Action after the time interval
        """
        raise NotImplementedError
