
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
    __slots__ = "row", "col"

    row: int
    col: int
    def __init__(self, row:int = 0, col:int = 0):
        self.row = row
        self.col = col


# Special value for distance
class TrackMark(Enum):
    Start = 0                   
    Finish = 65535             
    Init = 65000       


@dataclass 
class MarkLine :  
    __slots__ = "y_range", "x_range"

    y_range: range
    x_range: range

    def __init__(self, y_range:range, x_range:range):
        self.y_range = y_range
        self.x_range = x_range


class TrackField:
    __slots__ = ["field", "start_line", "finish_line"]

    field: np.ndarray
    start_line: MarkLine
    finish_line: MarkLine

    def __init__(self, row:int= 10, column:int = 10):
        self.field = np.zeros((row, column), dtype=np.dtype([('type', 'H'), ('distance', 'H')]))

    def fill_block(self, y_range: range, x_range: range , type: int, distance: int) :
        for y in y_range :
            for x in x_range :
                self.field[y, x]['type'] = type
                self.field[y, x]['distance'] = distance

    def mark_line(self, mark:TrackMark, line: MarkLine) :
        if mark == TrackMark.Start :
            self.start_line = line
        elif mark == TrackMark.Finish :
            self.finish_line = line

        for y in line.y_range :
            for x in line.x_range :
                self.field[y, x]['distance'] = mark.value
    
    def compute_track_distance(self):
        # Create a queue for BFS
        queue = []

		# Add the start line
        for y in self.start_line.y_range :
            for x in self.start_line.x_range :
                cell = TileCell(y, x)
                queue.append(cell)
                # print ('Init queue', cell)
        
        while queue:
            center = queue.pop(0)
            # print ('\ncenter', center)
            center_distance = self.field[center.row, center.col]['distance']

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


@dataclass
class CarView:
    __slots__ = ["up", "left", "field"]

    up: int
    left: int
    field: np.ndarray

    def __init__(self, track_field: TrackField, position: car.Point2D, view_radius: int) -> None:
        """
        Creates a new CarView:
            track_field: the complete track field
            position : car position, center of car view
            view_radius: car visible distance in any direction, in meter.
        """
        field = track_field.field

        left = int(position.x - view_radius)
        if left < 0 :
            left = 0
        self.left = left

        right = int(position.x + view_radius + 1)
        if right > field.shape[1] :
            right = field.shape[1]
        right = right

        up = int(position.y - view_radius)
        if up < 0 :
            up = 0
        self.up = up

        down = int(position.y + view_radius + 1)
        if down > field.shape[0] :
            down = field.shape[0]
        down = down

        # print('[', up, ':', down, '][', left, ':', right, ']')
        self.field = field[up:down, :][:, left:right]

