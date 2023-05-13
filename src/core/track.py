import numpy as np
from dataclasses import dataclass
from enum import Enum


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


@dataclass
class TrackInfo:

        name: str
        row: int
        column: int
        start_line: MarkLine
        finish_line: MarkLine
        round_distance: int
    
        def __init__(self, 
                name:str = 'trackinfo', 
                round_distance:int = 0, 
                row:int= 1, 
                column:int = 1, 
                start_line:MarkLine = None, 
                finish_line:MarkLine = None):
            
            self.type = 'TrackInfo'
            self.name = name
            self.row = row
            self.column = column
            self.start_line = start_line
            self.finish_line = finish_line
            self.round_distance = round_distance
    

@dataclass
class TrackField:

    track_info: TrackInfo 
    field: np.ndarray

    def __init__(self, row:int= 10, column:int = 10):
        self.track_info = TrackInfo()
        self.field = np.zeros((row, column), dtype=np.dtype([('type', 'H'), ('distance', 'H')]))


    def fill_block(self, y_range: range, x_range: range , type: int, distance: int) :
        for y in y_range :
            for x in x_range :
                self.field[y, x]['type'] = type
                self.field[y, x]['distance'] = distance

    def mark_line(self, line: MarkLine) :
        for y in line.y_range :
            for x in line.x_range :
                self.field[y, x]['distance'] = line.mark.value
    
    def compute_track_distance(self, start_line: MarkLine, finish_line: MarkLine):

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
        
        self.round_distance = 0 
        while queue:
            center = queue.pop(0)
            # print ('\ncenter', center)
            center_distance = int(self.field[center.row, center.col]['distance'])
            if center_distance > self.round_distance :
                self.round_distance = center_distance
                # print('round', self.round_distance)   
            
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

        self.round_distance += 2 # add 2 for start and finish line
    
    def get_track_view(self, position: car.Point2D, view_radius: int) -> TrackView:
        
        left = int(position.x - view_radius)
        if left < 0 :
            left = 0

        right = int(position.x + view_radius + 1)
        if right > self.field.shape[1] :
            right = self.field.shape[1]
        right = right

        up = int(position.y - view_radius)
        if up < 0 :
            up = 0

        down = int(position.y + view_radius + 1)
        if down > self.field.shape[0] :
            down = self.field.shape[0]
        down = down

        # print('[', up, ':', down, '][', left, ':', right, ']')
        field = self.field[up:down, :][:, left:right]

        return TrackView(up, left, field)
    