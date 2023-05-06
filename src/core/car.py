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
class MotionProfile:
    __slots__ = "max_acceleration", "max_velocity", "max_angular_velocity"

    max_acceleration: float         # max power produced acceleration in wheel forward direction m/s/s
    max_velocity: float             # wheel forward direction maximum velocity m/s
    max_angular_velocity: float     # radian/sec

    def __init__(self, 
            max_acceleration = 0, 
            max_velocity = 0,
            max_angular_velocity = 0):
        self.max_acceleration = max_acceleration
        self.max_velocity = max_velocity
        self.max_angular_velocity = max_angular_velocity


@dataclass
class CarConfig:
    __slots__ = "rotation_friction", "slide_friction", "motion_profile"

    rotation_friction: RotationFriction     # Rotational friction parameters
    slide_friction: SlideFriction           # Slide friction parameters
    motion_profile: MotionProfile           # limit on wheel acceleration and velocity

    def __init__(self, 
            rotation_friction = RotationFriction(), 
            slide_friction = SlideFriction(),
            motion_profile = MotionProfile()):

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
    __slots__ = "timestamp", "wheel_angle", "velocity_x", "velocity_y", "position",  "trackDistance"

    timestamp: int              # Milliseconds since race start

    wheel_angle: float          # whee angle, radian
    velocity_x: float           # m/s
    velocity_y: float           # m/s

    position: Point2D           # (x,y)
    trackDistance: int          # TrackDistance of the Tile it is on

    def __init__(self, 
            timestamp = 0, 
            wheel_angle = 0, 
            velocity_x = 0, 
            velocity_y = 0, 
            position = Point2D(), 
            trackDistance = 0):
        
        self.timestamp = timestamp

        self.wheel_angle = wheel_angle
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y

        self.position = position
        self.trackDistance = trackDistance


@dataclass
class Action:
    __slots__ = "acceleration_forward", "angular_velocity"

    acceleration_forward:float     # wheel forward acceleration
    angular_velocity: float        # wheel angle change rate
