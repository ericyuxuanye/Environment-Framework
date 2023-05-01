from dataclasses import dataclass


@dataclass
class RotationFriction:
    __slots__ = ["min_accel_start", "friction", "max_velocity"]

    min_accel_start: float
    """The minimum acceleration needed to start the car"""

    friction: float
    """The friction coefficient of the car"""

    max_velocity: float
    """The maximum velocity of the rotation of the car"""


@dataclass
class SlideFriction:
    __slots__ = ["min_velocity_start", "friction"]

    min_velocity_start: float
    """The minimum velocity needed to start the car"""

    friction: float
    """The friction coefficient"""


@dataclass
class CarConfig:
    __slots__ = ["rotation_friction", "slide_friction"]
    rotation_friction: RotationFriction
    """Rotational friction of the car"""
    slide_friction: SlideFriction
    """Slide friction of the car"""


@dataclass
class CarInfo:
    __slots__ = ["id", "team", "city", "state", "region"]
    id: int
    team: str
    city: str
    state: str
    region: str


@dataclass
class CarState:
    __slots__ = [
        "timestamp",
        "x_velocity",
        "y_velocity",
        "angular_velocity",
        "location",
        "angle",
        "distance",
    ]

    timestamp: int
    """Milliseconds since start of race"""

    x_velocity: float
    """x velocity (m/s)"""
    y_velocity: float
    """y velocity (m/s)"""
    angular_velocity: float
    """Angular velocity radians/sec"""

    location: tuple[int, int]
    """Point(x, y)"""
    angle: float
    """Angle of car in radians"""
    distance: float
    """Distance from start"""
