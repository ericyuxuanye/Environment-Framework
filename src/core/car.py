from dataclasses import dataclass
import math

@dataclass 
class Point2D :  
    x: float
    y: float

    def __init__(self, x:float = 0, y:float = 0):
        self.type = 'Point2D'
        self.x = x
        self.y = y


@dataclass
class RotationFriction:

    min_accel_start: float          # The minimum acceleration needed to start the car
    friction: float                 # The friction coefficient of the car

    def __init__(self, min_accel_start:float = 0, friction:float = 0):
        self.type = 'RotationFriction'
        self.min_accel_start = min_accel_start
        self.friction = friction


@dataclass
class SlideFriction:

    min_velocity_start: float       # Minimum velocity need to start slide sideway
    friction: float                 # Friction coefficient when sliding sideway

    def __init__(self, min_velocity_start=0, friction=0):
        self.type = 'SlideFriction'
        self.min_velocity_start = min_velocity_start
        self.friction = friction


@dataclass
class MotionProfile:

    max_acceleration: float         # max power produced acceleration in wheel forward direction m/s/s
    max_velocity: float             # wheel forward direction maximum velocity m/s
    max_angular_velocity: float     # radian/sec

    def __init__(self, 
            max_acceleration = 0, 
            max_velocity = 0,
            max_angular_velocity = 0):
        self.type = 'MotionProfile'
        self.max_acceleration = max_acceleration
        self.max_velocity = max_velocity
        self.max_angular_velocity = max_angular_velocity


@dataclass
class CarConfig:

    rotation_friction: RotationFriction     # Rotational friction parameters
    slide_friction: SlideFriction           # Slide friction parameters
    motion_profile: MotionProfile           # limit on wheel acceleration and velocity

    def __init__(self, 
            rotation_friction = RotationFriction(), 
            slide_friction = SlideFriction(),
            motion_profile = MotionProfile()):
        self.type = 'CarConfig'
        self.rotation_friction = rotation_friction
        self.slide_friction = slide_friction
        self.motion_profile = motion_profile


@dataclass
class CarInfo:

    id: int
    team: str
    city: str
    state: str
    region: str

    def __init__(self, id = 0, team = '', city = '', state = '', region = ''):
        self.type = 'CarInfo'
        self.id = id
        self.team = team
        self.city = city
        self.state = state
        self.region = region


@dataclass
class CarState:

    timestamp: int              # Milliseconds since race start

    wheel_angle: float          # whee angle, radian
    velocity_x: float           # m/s
    velocity_y: float           # m/s

    velocity_distance: float    # polar coordinate velocity distance
    velocity_angle_wheel: float # polar coordinate velocity angle relative to wheel_angle
    rays:list[float]            # list of ray distance

    position: Point2D           # (x,y)
    tile_type: int              # tile type of the Tile it is on
    tile_distance: int          # distance from the start of the track
    round_count: int            # full track round completed
    max_round_distance: int     # max distance from the start of the track in a round
    max_total_distance: int     # max total distance from the start, = round_count * track_info.round_distance + max_round_distance

    def __init__(self, 
            timestamp:int = 0, 
            wheel_angle:float = 0, 
            velocity_x:float = 0, 
            velocity_y :float = 0,
            velocity_distance: float = 0,    
            velocity_angle_wheel: float = 0,       
            rays:list[float] = [],           
            position = Point2D(),
            tile_type:int = 0,
            tile_distance:int = 0,
            round_count:int = 0,
            max_round_distance:int = 0,
            max_total_distance:int = 0):

        self.type = 'CarState'
        self.timestamp = timestamp

        self.wheel_angle = wheel_angle
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.velocity_distance = velocity_distance
        self.velocity_angle_wheel = velocity_angle_wheel
        self.rays = rays        

        self.position = position
        self.tile_type = tile_type
        self.tile_distance = tile_distance
        self.round_count = round_count
        self.max_round_distance = max_round_distance
        self.max_total_distance = max_total_distance
    
    def calc_velocity_polar(self)->None:
        self.velocity_distance = math.sqrt(self.velocity_x**2 + self.velocity_y**2)
        self.velocity_angle_wheel = math.atan2(self.velocity_y, self.velocity_x) - self.wheel_angle


@dataclass
class Action:

    forward_acceleration: float     # wheel forward acceleration
    angular_velocity: float         # wheel angle change rate

    def __init__(self, forward_acceleration=0, angular_velocity=0):
        self.type = 'Action'
        self.forward_acceleration = forward_acceleration
        self.angular_velocity = angular_velocity