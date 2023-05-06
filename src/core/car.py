from dataclasses import dataclass

@dataclass 
class Point2D :  
    __slots__ = "x", "y"

    x: float
    y: float

    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y


@dataclass
class RotationFriction:
    __slots__ = "min_accel_start", "friction", "max_velocity"

    min_accel_start: float          # The minimum acceleration needed to start the car
    friction: float                 # The friction coefficient of the car
    max_velocity: float             # The maximum velocity of the rotation of the car

    def __init__(self, min_accel_start=0, friction=0, max_velocity=0):
        self.min_accel_start = min_accel_start
        self.friction = friction
        self.max_velocity = max_velocity


@dataclass
class SlideFriction:
    __slots__ = "min_velocity_start", "friction"

    min_velocity_start: float       # Minimum velocity need to start slide sideway
    friction: float                 # Friction coefficient when sliding sideway

    def __init__(self, min_velocity_start=0, friction=0):
        self.min_velocity_start = min_velocity_start
        self.friction = friction


@dataclass
class CarConfig:
    __slots__ = "rotation_friction", "slide_friction"

    rotation_friction: RotationFriction     # Rotational friction parameters
    slide_friction: SlideFriction           # Slide friction parameters

    def __init__(self, rotation_friction = RotationFriction(), slide_friction = SlideFriction()):
        self.rotation_friction = rotation_friction
        self.slide_friction = slide_friction


@dataclass
class CarInfo:
    __slots__ = "id", "team", "city", "state", "region"
    id: int
    team: str
    city: str
    state: str
    region: str

    def __init__(self, id = 0, team = '', city = '', state = '', region = ''):
        self.id = id
        self.team = team
        self.city = city
        self.state = state
        self.region = region


@dataclass
class CarState:
    __slots__ = "timestamp", "heading", "forward_velocity", "slide_velocity", "position",  "trackDistance"

    timestamp: int              # Milliseconds since race start

    heading: float              # forward angle, radian
    forward_velocity: float     # m/s, at 
    slide_velocity: float       # m/s

    position: Point2D           # (x,y)

    trackDistance: int          # TrackDistance of the Tile it is on

    def __init__(self, 
            timestamp = 0, 
            heading = 0, 
            forward_velocity = 0, 
            slide_velocity = 0, 
            position = Point2D(), 
            trackDistance = 0):
        
        self.timestamp = timestamp

        self.heading = heading
        self.forward_velocity = forward_velocity
        self.slide_velocity = slide_velocity

        self.position = position
        self.trackDistance = trackDistance


@dataclass
class Action:
    __slots__ = "forward_acceleration", "angular_velocity"

    forward_acceleration:float     # wheel forward direction acceleration
    angular_velocity: float        # wheel angle change rate
