from dataclasses import dataclass
from math import atan2, cos, sin, sqrt

import numpy as np
from car import CarConfig, CarState, Point2D
from model import Action

"""
This is the characteristics of the track. This file acts as the main physics engine.

A track field consists of equally sized tiles, with upper left corner as (0, 0).

A [500, 2000] track field has, upper right corner at (0, 1999),
lower left corner at (499, 0), and lower right corner at (499, 1999)
"""


FieldTile = np.dtype([("type_id", np.uint8), ("distance", np.float64)])

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

    def __init__(
        self, track_field: TrackField, x: int, y: int, view_distance: int
    ) -> None:
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
    __slots__ = ["track_field", "view_distance"]
    track_field: TrackField
    view_distance: int

    def __init__(self, track_field=TrackField(), view_distance=3):
        self.track_field = track_field
        self.view_distance = view_distance

    def get_car_view(self, state: CarState) -> CarView:
        """
        return subsection of TrackField visible to car at position of CarState.
        """
        return CarView(
            self.track_field,
            round(state.location.x),
            round(state.location.y),
            self.view_distance,
        )

    def get_next_state(
        self,
        state: CarState,
        action: Action,
        interval: int,
        config: CarConfig = CarConfig(),
    ):
        """
        Returns the CarState using the Action after the time interval
        """
        x, y = state.location.x, state.location.y
        angle = state.angle
        x_velocity = state.x_velocity
        y_velocity = state.y_velocity

        if (
            abs(action.angular_velocity) > config.rotation_friction.min_accel_start
            and abs(action.angular_velocity) > config.rotation_friction.friction
        ):
            # we have overcome friction to move
            angle_delta = (
                action.angular_velocity - config.rotation_friction.friction
                if action.angular_velocity > 0
                else action.angular_velocity + config.rotation_friction.friction
            )
            # clip the maximum velocity
            angle_delta = max(
                min(angle_delta, -config.rotation_friction.max_velocity),
                config.rotation_friction.max_velocity,
            )
            angle += angle_delta * interval

        # convert velocity to polar
        velocity_r = sqrt(x_velocity * x_velocity + y_velocity * y_velocity)
        velocity_theta = atan2(y_velocity, x_velocity)
        # add speed in car's heading direction and subtract speed from friction
        velocity_r += (
            action.linear_acceleration - config.slide_friction.friction
        ) * interval
        # speed should not be negative (r is always positive)
        velocity_r = max(velocity_r, 0)

        # change back to cartesian coordinates
        x_velocity = velocity_r * cos(velocity_theta)
        y_velocity = velocity_r * sin(velocity_theta)

        # move car only if velocity is enough
        if velocity_r >= config.slide_friction.min_velocity_start:
            x += x_velocity * interval
            y += y_velocity * interval

        x, y = round(x), round(y)

        return CarState(
            state.timestamp + interval,
            round(x_velocity),
            round(y_velocity),
            Point2D(x, y),
            round(angle),
            self.track_field.field[x, y]["distance"],
        )
