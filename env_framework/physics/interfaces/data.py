import numpy as np
from dataclasses import dataclass


@dataclass
class CarView:
    __slots__ = ["up_left"]
    """
    The location of the car (x, y)
    """
    up_left: tuple[float, float]
    """
    A subsection of the entire track field
    """
    field: np.ndarray


@dataclass
class CarState:
    __slots__ = ["velocity", "direction"]
    """
    The velocity of the car (Vx, Vy)
    """
    velocity: tuple[float, float]
    """
    The heading of the car (counterclockwise radians from right)
    """
    direction: float


@dataclass
class CarConfig:
    __slots__ = ["acceleration", "friction"]
    """
    The amount of acceleration that the car has
    """
    acceleration: float

    """
    The friction of the car tires
    """
    friction: float


@dataclass
class TileConfig:
    __slots__ = ["config"]
    """
    The configuration for the tiles.

    This is a list of different tile types, where the index is the tile's type.
    Each index of the list contains two numbers, the amount of friction
    and the amount of rotation
    """
    config: list[tuple[float, float]]


@dataclass
class Action:
    __slots__ = ["power", "steer"]

    """
    The power applied to the car
    """
    power: float

    """
    The amount of steering applied to the car
    """
    steer: float


class TrackField:
    __slots__ = ["field"]
    """
    The entire track field
    """
    field: np.ndarray
