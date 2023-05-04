from dataclasses import dataclass, field

@dataclass(slots=True)
class Point2D :  
    x: float = 0.
    y: float = 0.


@dataclass(slots=True)
class RotationFriction:
    min_accel_start: float = 0.          # The minimum acceleration needed to start the car
    friction: float = 0.                 # The friction coefficient of the car
    max_velocity: float = 0.             # The maximum velocity of the rotation of the car

@dataclass(slots=True)
class SlideFriction:
    min_velocity_start: float = 0.       # Minimum velocity need to start slide sideway
    friction: float = 0.                 # Friction coefficient when sliding sideway

@dataclass(slots=True)
class CarConfig:
    rotation_friction: RotationFriction = field(default_factory=RotationFriction)  # Rotational friction parameters
    slide_friction: SlideFriction = field(default_factory=SlideFriction)           # Slide friction parameters

@dataclass(slots=True)
class CarInfo:
    id: int = 0
    team: str = ''
    city: str = ''
    state: str = ''
    region: str = ''


@dataclass(slots=True)
class CarState:
    timestamp: int = 0                                  # Milliseconds since race start

    x_velocity: float = 0.                              # m/s
    y_velocity: float = 0.                              # m/s

    location: Point2D = field(default_factory=Point2D)  # (x,y)
    angle: float = 0.                                   # heading angle, radian

    trackDistance: int = 0                              # TrackDistance of the Tile it is on
