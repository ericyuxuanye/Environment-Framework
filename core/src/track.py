import numpy as np
from dataclasses import dataclass
from enum import Enum
import math

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


@dataclass 
class TileCell :  

    row: int
    col: int
    def __init__(self, row:int = 0, col:int = 0):
        self.type = 'TileCell'
        self.row = row
        self.col = col


# Special value for distance
class TrackMark(Enum):
    Start = 0                   
    Finish = 65535             
    Init = 65000       


@dataclass 
class MarkLine :  
    mark: TrackMark
    y_range: range
    x_range: range

    def __init__(self, mark: TrackMark, y_range:range, x_range:range):
        self.type = 'MarkLine'
        self.mark = mark
        self.y_range = y_range
        self.x_range = x_range

"""
@dataclass
class TrackView:

    up: int
    left: int
    field: np.ndarray

    def __init__(self, up:int = 0, left:int = 0, field:np.ndarray = None):
        self.type = 'TrackView'
        self.up = up
        self.left = left
        self.field = field
"""

@dataclass
class TrackInfo:

        name: str
        row: int
        column: int
        round_distance: int
        view_radius : int
        time_interval : int # msec
    
        def __init__(self, 
                name:str = 'trackinfo', 
                round_distance:int = 0, 
                row:int= 1, 
                column:int = 1,
                view_radius:int = 1,
                time_interval:int = 100):
            
            self.type = 'TrackInfo'
            self.name = name
            self.row = row
            self.column = column
            self.view_radius = view_radius
            self.time_interval = time_interval
            self.round_distance = round_distance
    

@dataclass
class TrackField:

    track_info: TrackInfo 
    field: np.ndarray

    def __init__(self, track_info: TrackInfo):
        self.track_info = track_info
        self.field = np.zeros((track_info.row, track_info.column), dtype=np.dtype([('type', 'H'), ('distance', 'H')]))


    def fill_block(self, y_range: range, x_range: range , type: int, distance: int) :
        for y in y_range :
            for x in x_range :
                self.field[y, x]['type'] = type
                self.field[y, x]['distance'] = distance

    def mark_line(self, line: MarkLine) :
        for y in line.y_range :
            for x in line.x_range :
                self.field[y, x]['distance'] = line.mark.value
    
    
    def compute_tile_distance(self, start_line: MarkLine, finish_line: MarkLine):

        self.mark_line(start_line)
        self.mark_line(finish_line)

        # Create a queue for BFS
        queue = []

		# Add the start line
        for y in start_line.y_range :
            for x in start_line.x_range :
                cell = TileCell(y, x)
                queue.append(cell)
                # print ('Init queue', cell)
        
        self.track_info.round_distance = 0 
        while queue:
            center = queue.pop(0)
            # print ('\ncenter', center)
            center_distance = int(self.field[center.row, center.col]['distance'])
            if center_distance > self.track_info.round_distance :
                self.track_info.round_distance = center_distance
                # print('round', self.track_info.round_distance)   
            
            for y in [-1,0,1] :
                for x in [-1,0,1] :
                    if y == 0 and x == 0:
                        continue    # center
                    
                    target = TileCell(center.row + y, center.col + x)
                    if target.row < 0 or target.row >= self.field.shape[0] :
                        continue # row out of bound
                    if target.col < 0 or target.col >= self.field.shape[1] :
                        continue # col out of bound
                    if self.field[target.row, target.col]['type'] != TileType.Road.value :
                        continue # only deal with bound
                    if self.field[target.row, target.col]['distance'] == TrackMark.Finish.value :
                        continue # finish line
                    if self.field[target.row, target.col]['distance'] == TrackMark.Init.value :
                        queue.append(target)
                        # print('append queue', target) 

                    target_distance = self.field[target.row, target.col]['distance']
                    if target_distance > center_distance + 1 :
                        self.field[target.row, target.col]['distance'] = center_distance + 1
                        # print (target, " update:", target_distance, '=>', self.field[target.row, target.col]['distance'])

        self.track_info.round_distance += 2 # add 2 for start and finish line
    
    """
    def get_track_view(self, position:car.Point2D) -> TrackView:
        
        left = int(position.x - self.track_info.view_radius)
        if left < 0 :
            left = 0

        right = int(position.x + self.track_info.view_radius + 1)
        if right > self.field.shape[1] :
            right = self.field.shape[1]
        right = right

        up = int(position.y - self.track_info.view_radius)
        if up < 0 :
            up = 0

        down = int(position.y + self.track_info.view_radius + 1)
        if down > self.field.shape[0] :
            down = self.field.shape[0]
        down = down

        # print('[', up, ':', down, '][', left, ':', right, ']')
        field = self.field[up:down, :][:, left:right]

        return TrackView(up, left, field)
    """

    def calc_track_state(self, car_state:car.CarState) -> None:

        if car_state.wheel_angle > math.pi :
            car_state.wheel_angle -= math.pi*2
        elif car_state.wheel_angle < -math.pi :
            car_state.wheel_angle += math.pi*2

        track_state = car_state.track_state
        track_state.velocity_distance = math.sqrt(car_state.velocity_x**2 + car_state.velocity_y**2)

        track_state.velocity_angle_to_wheel = math.atan2(car_state.velocity_y, car_state.velocity_x) - car_state.wheel_angle
        if track_state.velocity_angle_to_wheel > math.pi :
            track_state.velocity_angle_to_wheel -= math.pi*2
        elif track_state.velocity_angle_to_wheel < -math.pi :
            track_state.velocity_angle_to_wheel += math.pi*2
    
        cell = TileCell(int(car_state.position.y), int(car_state.position.x))
        track_state.tile_type = int(self.field[cell.row, cell.col]['type'])
        track_state.tile_distance = int(self.field[cell.row, cell.col]['distance'])
        if track_state.tile_type == TileType.Road.value and track_state.tile_distance == TrackMark.Finish.value:
            track_state.tile_distance = self.track_info.round_distance - 1
        if track_state.tile_type == TileType.Road.value :
            track_state.tile_total_distance = self.track_info.round_distance * car_state.round_count + track_state.tile_distance  
        else:
            track_state.tile_total_distance = 0
        
        last_road_cell = TileCell(int(car_state.last_road_position.y), int(car_state.last_road_position.x))
        track_state.last_road_tile_distance = int(self.field[last_road_cell.row, last_road_cell.col]['distance'])
        if (int(self.field[last_road_cell.row, last_road_cell.col]['type']) == TileType.Road.value 
            and track_state.last_road_tile_distance == TrackMark.Finish.value):
            track_state.last_road_tile_distance = self.track_info.round_distance - 1
        track_state.last_road_tile_total_distance = self.track_info.round_distance * car_state.round_count + track_state.last_road_tile_distance  

        angles = [0, -math.pi/2, math.pi/2, -math.pi/4, math.pi/4, -math.pi*1/8, math.pi*1/8, -math.pi*3/8, math.pi*3/8]
        track_state.rays = []
        for angle in angles:
            track_state.rays.append(self.get_ray(car_state.position.x, car_state.position.y, car_state.wheel_angle, angle))  

       
    def get_next_state(self, 
            car_config: car.CarConfig, 
            car_state: car.CarState, 
            action: car.Action, 
            debug: bool = False) -> car.CarState :
        
        if debug: 
            print('\nget_next_state() >>>')

        # Limit action by motion profile
        action_forward_acceleration = action.forward_acceleration
        if abs(action.forward_acceleration) > car_config.motion_profile.max_acceleration :
            action_forward_acceleration = (car_config.motion_profile.max_acceleration 
                * action.forward_acceleration / abs(action.forward_acceleration))
        if debug:
            print('action_forward_acceleration = ', action_forward_acceleration)

        angular_velocity = action.angular_velocity
        if abs(action.angular_velocity) > car_config.motion_profile.max_angular_velocity :
            action_forward_acceleration = (car_config.motion_profile.max_angular_velocity 
                * action.angular_velocity / abs(action.angular_velocity))
        if debug:
            print('angular_velocity = ', angular_velocity)

        # next position
        time_sec:float = 0.001 * self.track_info.time_interval
        next_position = car.Point2D(
            x = car_state.position.x + car_state.velocity_x * time_sec, 
            y = car_state.position.y + car_state.velocity_y * time_sec)
        
        if (next_position.x >= self.field.shape[1]) :
            next_position.x = self.field.shape[1] - .5
        if (next_position.x < 0) :
            next_position.x = .5
        if (next_position.y >= self.field.shape[0]) :    
            next_position.y = self.field.shape[0] - .5      
        if (next_position.y < 0) :
            next_position.y = .5
        if debug:
            print('next_position = ', next_position)

        next_cell = TileCell(int(next_position.y), int(next_position.x))
        next_cell_type = int(self.field[next_cell.row, next_cell.col]['type'])
        next_tile_distance = int(self.field[next_cell.row, next_cell.col]['distance'])
        if next_cell_type == TileType.Road.value :
            last_road_position = next_position
        else:
            last_road_position = car_state.last_road_position

        next_state = car.CarState(
            timestamp = car_state.timestamp + self.track_info.time_interval,
            wheel_angle = car_state.wheel_angle + angular_velocity * time_sec,
            position = next_position,
            last_road_position = last_road_position,
            round_count = car_state.round_count)

        # next velocity
        velocity_forward: float = (car_state.velocity_x * math.cos(0 - car_state.wheel_angle) 
            + car_state.velocity_y * math.cos(math.pi / 2 - car_state.wheel_angle))
        if debug: 
            print('velocity_forward = ', velocity_forward)

        velocity_slide_right: float = (car_state.velocity_y * math.sin(math.pi / 2 - car_state.wheel_angle) 
            + car_state.velocity_x * math.sin(0 - car_state.wheel_angle))
        if abs(velocity_slide_right) <= car_config.slide_friction.min_velocity_start :
            velocity_slide_right = 0
        if debug: 
            print('velocity_slide_right = ', velocity_slide_right)
    
        cell = TileCell(int(car_state.position.y), int(car_state.position.x))
        cell_type = self.field[cell.row, cell.col]['type']

        tile_distance = int(self.field[cell.row, cell.col]['distance'])

        if (cell_type == TileType.Road.value 
            and next_cell_type == TileType.Road.value):
                if (tile_distance == TrackMark.Start.value
                    and next_tile_distance == TrackMark.Finish.value) :
                    next_state.round_count = car_state.round_count - 1        # start to finish backward, decrease a round
                if (tile_distance == TrackMark.Finish.value 
                    and next_tile_distance == TrackMark.Start.value) :
                    next_state.round_count = car_state.round_count + 1        # finish to start, complete a round
        if debug: 
            print('next cell_type = ', next_cell_type, 'next_tile_distance = ', next_tile_distance)
            
            if next_state.round_count != car_state.round_count: 
                print('from cell', cell , 'Tile', self.field[cell.row, cell.col], 
                    'round_count', car_state.round_count,
                    'to cell', next_cell, 'Tile', self.field[next_cell.row, next_cell.col], 
                    'round_count', next_state.round_count)

        friction_ratio = cell_type
        if debug: 
            print('cell', cell, 'cell_type', cell_type, 'friction_ratio = ', friction_ratio)

        acceleration_forward: float = 0
        if velocity_forward != 0:
            acceleration_forward = (action_forward_acceleration 
                - car_config.rotation_friction.friction * friction_ratio)
        elif action_forward_acceleration >= car_config.rotation_friction.min_accel_start :
            acceleration_forward = (action_forward_acceleration 
                - car_config.rotation_friction.friction * friction_ratio)
        if debug: 
            print('acceleration_forward = ', acceleration_forward)

        acceleration_slide_right:float = 0
        if abs(velocity_slide_right) > car_config.slide_friction.min_velocity_start :
            if velocity_slide_right > 0 :
                acceleration_slide_right = -1 * car_config.slide_friction.friction * friction_ratio
            else :
                acceleration_slide_right = car_config.slide_friction.friction * friction_ratio
        if debug: 
            print('acceleration_slide_right = ', acceleration_slide_right)
    
        next_velocity_forward = velocity_forward + acceleration_forward * time_sec
        # never rotate backward
        if next_velocity_forward < 0 :
            next_velocity_forward = 0

        if debug:
            print('before limit, next_velocity_forward = ', next_velocity_forward)
        if next_velocity_forward > car_config.motion_profile.max_velocity:
            next_velocity_forward = car_config.motion_profile.max_velocity 
        if debug: 
            print('after limit, next_velocity_forward = ', next_velocity_forward)

        next_velocity_slide_right = velocity_slide_right + acceleration_slide_right * time_sec
        if (next_velocity_slide_right * velocity_slide_right < 0) :
            next_velocity_slide_right = 0
        if debug: 
            print('next_velocity_slide_right = ', next_velocity_slide_right)

        next_state.velocity_x = (next_velocity_forward * math.cos(car_state.wheel_angle)
            + next_velocity_slide_right * math.cos(car_state.wheel_angle + math.pi / 2))
        next_state.velocity_y = (next_velocity_forward * math.sin(car_state.wheel_angle)
            + next_velocity_slide_right * math.sin(car_state.wheel_angle + math.pi / 2))

        if debug: 
            print('get_next_state() <<<\n')

        self.calc_track_state(next_state)
        return next_state

    
    def get_ray(self, position_x:float, position_y:float, wheel_angle:float, ray_angle:float, debug=False) -> float:

        target_angle = wheel_angle + ray_angle

        use_x = abs(math.cos(target_angle)) >= abs(math.sin(target_angle))
        if debug:
            print('position_x = ', position_x
                , ', position_y = ', position_y
                , ', target_angle = ', target_angle
                , ', use_x = ', use_x)
            
        if use_x:
            step_x = abs(math.cos(target_angle))/math.cos(target_angle)
            step_y = math.tan(target_angle)
            if debug:
                print('step_x = ', step_x, 'step_y = ', step_y)
                
            for step in range(self.track_info.column):
                x = position_x + step * step_x
                y = position_y + step * step_x * step_y

                cell = TileCell(int(y), int(x))
                if debug:
                    print('x = ', x, ', y = ', y, ', cell = ', cell)
            
                if cell.row < 0 or cell.row >= self.track_info.row or cell.col < 0 or cell.col >= self.track_info.column:
                    return 0

                tile_type = self.field[cell.row, cell.col]['type']
                if debug:
                    print('tile_type = ', tile_type)
                if tile_type == TileType.Wall.value:
                    if position_x < x :
                        x_edge = int(x)
                    else:
                        x_edge = int(x) + 1

                    y_edge = ( x_edge - position_x) /step_x * step_y + position_y
                    if int(y) <= y_edge and y_edge <= int(y) + 1:
                        if debug:
                            print('vertial: x_edge = ', x_edge, ', y_edge = ', y_edge)
                        return math.sqrt((x_edge - position_x)**2 + (y_edge - position_y)**2)
                    
                    if position_y < y :
                        y_edge = int(y)
                    else:
                        y_edge = int(y) + 1
                    x_edge = (y_edge - position_y) / step_y * step_x + position_x
                    if debug:
                        print('horizontal: x_edge = ', x_edge, ', y_edge = ', y_edge)
                    return math.sqrt((x_edge - position_x)**2 + (y_edge - position_y)**2)
        else:
            step_y = abs(math.sin(target_angle))/math.sin(target_angle)
            step_x = math.cos(target_angle) / math.sin(target_angle)

            if debug:
                print('step_x = ', step_x, 'step_y = ', step_y)
                
            for step in range(self.track_info.row):
                y = position_y + step * step_y
                x = position_x + step * step_y * step_x
            
                cell = TileCell(int(y), int(x))
                if debug:
                    print('x = ', x, ', y = ', y, ', cell = ', cell)
            
                if cell.row < 0 or cell.row >= self.track_info.row or cell.col < 0 or cell.col >= self.track_info.column:
                    return 0

                tile_type = self.field[cell.row, cell.col]['type']
                if debug:
                    print('tile_type = ', tile_type)
                if tile_type == TileType.Wall.value:
                    if position_y < y :
                        y_edge = int(y)
                    else:
                        y_edge = int(y) + 1

                    x_edge = (y_edge - position_y) * step_x + position_x
                    if debug:
                        print('x_edge = ', x_edge, ', y_edge = ', y_edge)
                    if int(x) <= x_edge and x_edge <= int(x) + 1:
                        if debug:
                            print('horizontal, use x_edge = ', x_edge, ', y_edge = ', y_edge)
                        return math.sqrt((x_edge - position_x)**2 + (y_edge - position_y)**2)
                    
                    if position_x < x :
                        x_edge = int(x)
                    else:
                        x_edge = int(x) + 1
                    y_edge = (x_edge - position_x) / step_x * step_y + position_y
                    if debug:
                        print('vertial: x_edge = ', x_edge, ', y_edge = ', y_edge)
                    return math.sqrt((x_edge - position_x)**2 + (y_edge - position_y)**2)

                        

