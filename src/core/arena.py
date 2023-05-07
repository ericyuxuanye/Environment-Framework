
import numpy as np
from dataclasses import dataclass
from enum import Enum
import math

from . import car
from . import track

"""
Arena acts as physics engine.

A track field consists of equally sized tiles, with upper left corner as (0, 0).

A [500, 2000] track field has, upper right corner at (0, 1999),
lower left corner at (499, 0), and lower right corner at (499, 1999)
"""

"""
TrackSystem acts as the physics engine.

It owns the TrackField, CarView radius. 

Usage:
    1. Construct TrackField, specify dimision, populate each tile type
    2. Specify Starting and Ending tiles
        Tiles between Starting and Ending tiles are properly edged on all side of the path
        Starting and Ending tiles can be same for round track. 
    3. Calculate distance for all road tiles. After this, the TrackSystem is initialized.



"""

class Arena:

    track_field : track.TrackField
    view_radius : int
    car_config : car.CarConfig
    
    def __init__(self, 
            track_field: track.TrackField, 
            view_radius: int,
            car_config : car.CarConfig = car.CarConfig()) -> None:
        self.track_field = track_field
        self.view_radius = view_radius
        self.car_config = car_config


    def get_car_view(self, car_state: car.CarState) -> track.CarView:
        return track.CarView(self.track_field, car_state.position, self.view_radius)
    
    
    def get_next_state(
            self, 
            car_state: car.CarState, 
            action: car.Action, 
            time_interval: int, 
            debug: bool = False) -> car.CarState :
        
        return self.__get_next_state(self.car_config, car_state, action, time_interval, debug)


    def __get_next_state(
            self, 
            car_config: car.CarConfig, 
            car_state: car.CarState, 
            action: car.Action, 
            time_interval: int,
            debug: bool = False) -> car.CarState :
        
        if debug: 
            print('get_next_state() >>>n')

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
        time_sec:float = 0.001 * time_interval
        next_position = car.Point2D(
            x = car_state.position.x + car_state.velocity_x * time_sec, 
            y = car_state.position.y + car_state.velocity_y * time_sec)
        next_cell = track.TileCell(int(next_position.y), int(next_position.x))
        next_state = car.CarState(
            timestamp = car_state.timestamp + time_interval,
            wheel_angle = car_state.wheel_angle + angular_velocity * time_sec,
            position = next_position,
            trackDistance = self.track_field.field[next_cell.row, next_cell.col]['distance'])

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
    
        cell = track.TileCell(int(car_state.position.y), int(car_state.position.x))
        friction_ratio = self.track_field.field[cell.row, cell.col]['type']
        # print('friction_ratio = ', friction_ratio)

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
        if debug: 
            print('next_velocity_slide_right = ', next_velocity_slide_right)

        next_state.velocity_x = (next_velocity_forward * math.cos(car_state.wheel_angle)
            + next_velocity_slide_right * math.cos(car_state.wheel_angle + math.pi / 2))
        next_state.velocity_y = (next_velocity_forward * math.sin(car_state.wheel_angle)
            + next_velocity_slide_right * math.sin(car_state.wheel_angle + math.pi / 2))

        if debug: 
            print('get_next_state() <<<\n')
        return next_state



