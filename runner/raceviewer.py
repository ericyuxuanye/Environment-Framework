import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import math
import numpy as np
from scipy.interpolate import make_interp_spline    
import PySimpleGUI as sg

from core.src import jsoner
from core.src.race import RaceData
from core.src.track import TileType, TrackField, TileCell

class CarElement:
    def __init__(self, graph, scale):
        self.graph = graph
        self.scale = scale
        self.radius = scale/2

    def show_step(self, step_data):
        position_x = step_data[3]
        position_y = step_data[4]
        angle = step_data[5]

        self.circle_figure = self.graph.DrawCircle(
            [position_x * self.scale, position_y * self.scale], 
            self.radius, 
            fill_color='blue', 
            line_color='blue'
        )

        angle_x = math.cos(angle) + position_x
        angle_y = math.sin(angle) + position_y
        self.angle_figure = self.graph.DrawLine(
            [position_x * self.scale, position_y * self.scale],
            [angle_x * self.scale, angle_y * self.scale],
            color = 'white', 
            width = 2
        )

    def move_to(self, step_data):
        position_x = step_data[3]
        position_y = step_data[4]
        angle = step_data[5]

        self.graph.delete_figure(self.circle_figure)
        self.circle_figure = self.graph.DrawCircle(
            [position_x * self.scale, position_y * self.scale], 
            self.radius, 
            fill_color='blue', 
            line_color='blue'
        )

        self.graph.delete_figure(self.angle_figure)
        angle_x = math.cos(angle) + position_x
        angle_y = math.sin(angle) + position_y
        self.angle_figure = self.graph.DrawLine(
            [position_x * self.scale, position_y * self.scale],
            [angle_x * self.scale, angle_y * self.scale],
            color = 'white', 
            width = 2
        )


class Viewer:
    def __init__(self,  track_field: TrackField, race_data: RaceData):
        self.track_field = track_field
        self.race_data = race_data
        self.init_config()
    
        self.interpolate_data()
        self.init_components()

    def init_config(self):
        self.window_width = 800           
        self.window_height = 600	
        self.scale = 20
        self.step_rate = 1
        self.show_cell = False
        
        self.road_color = 'green'
        self.shoulder_color = 'yellow'
        self.wall_color = 'red'
        self.start_color = 'white'
        self.finish_color = 'lightblue'

    def init_components(self):
        track_info = self.track_field.track_info

        field_width, field_height = track_info.column * self.scale, track_info.row * self.scale
        self.graph = sg.Graph(
            canvas_size=(field_width, field_height), 
            graph_bottom_left=(0, field_height), 
            graph_top_right=(field_width, 0), 
            background_color='white', 
            key='graph', 
            tooltip='track field')
        
        table = sg.Table(
            values=self.table_data, 
            headings=['sec', 'acceleration', 'angular velocity', 'x', 'y', 'angle'], 
            key='table',
            num_rows=10,
            display_row_numbers=True,
            justification = "right",
            background_color ='gray',
            alternating_row_color='teal',
            )

        self.layout = [
            [sg.Text(race_data.race_info.id, text_color='white', font=('Helvetica', 25))],
            [self.graph],
            [sg.Text('0'), sg.ProgressBar(max_value=self.steps_data.shape[0], orientation='h', size=(20, 20), key='progress_bar'), sg.Text(self.steps_data.shape[0])],
            [sg.Button('Play'), sg.Button('Step'), sg.Text('0', key='at_step'), sg.Exit()],
            [table],
            ]
        
        self.window = sg.Window(
            'Race Viewer', 
            self.layout, 
            element_justification='center', 
            grab_anywhere=True, 
            finalize=True
        )

        self.draw_track_field()
        self.car_element = CarElement(self.graph, self.scale)


    def draw_track_field(self):
        for y in range(self.track_field.track_info.row) :
            for x in range(self.track_field.track_info.column) :
                if self.track_field.field[y, x]['type'] == TileType.Wall.value:
                    tile_color = self.wall_color
                elif self.track_field.field[y, x]['type'] == TileType.Road.value:
                    tile_color = self.road_color
                elif self.track_field.field[y, x]['type'] == TileType.Shoulder.value:
                    tile_color = self.shoulder_color

                cell = TileCell(y, x)
                if self.track_field.is_start(cell):
                    tile_color = self.start_color
                elif self.track_field.is_finish(cell):
                    tile_color = self.finish_color
                
                self.graph.DrawRectangle(
                    (x * self.scale, y * self.scale), 
                    (x * self.scale + self.scale, y * self.scale + self.scale), 
                    fill_color = tile_color, 
                    line_color = 'gray', 
                    line_width = 1)
                
                if self.show_cell:
                    self.graph.DrawText(
                        self.track_field.field[y, x]['distance'], 
                        ((x+.5) * self.scale, (y+.5) * self.scale), 
                        color='black', 
                        font=('Helvetica', 10)
                    )


    def interpolate_data(self):
        steps = self.race_data.steps
        data = np.empty((len(steps), 6))
        for i, entry in enumerate(steps):
            data[i, 0] = entry.car_state.timestamp/1000.0
            data[i,1:3] = entry.action.forward_acceleration, entry.action.angular_velocity
            data[i,3:6] = entry.car_state.position.x, entry.car_state.position.y, entry.car_state.wheel_angle

        if self.step_rate == 1:
            self.steps_data = data
        else:
            new_data = np.linspace(0, len(steps) - 1, len(steps) * self.step_rate)
            self.steps_data = make_interp_spline(np.arange(len(steps)), data)(new_data)

        self.table_data = [[j for j in range(self.steps_data.shape[1])] for i in range(self.steps_data.shape[0])]
        for row in range(self.steps_data.shape[0]):
            for col in range(0, self.steps_data.shape[1]):
                self.table_data[row][col] = "{:.3f}".format(self.steps_data[row, col])


    def run(self):
        if (self.steps_data.shape[0] > 0):
            self.car_element.show_step(self.steps_data[0])
        
        at:int = 0
        play:bool = False
        while True:
            event, values = self.window.read(timeout=100/self.step_rate)
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == 'Step':
                play = False
                at += 1
                if at < self.steps_data.shape[0]:
                    self.car_element.move_to(self.steps_data[at])
                else:
                    at = 0
                    play = False
            
            if event == 'Play':
                play = True
            
            if play:
                at += 1
                if at < self.steps_data.shape[0]:
                    self.car_element.move_to(self.steps_data[at])
                else:
                    at = 0
                    play = False

            self.window['progress_bar'].update(at)
            self.window['at_step'].update(at)

        self.window.close()

if __name__ == "__main__":
    data_folder = sg.popup_get_folder(
        'Select race data folder', 
        default_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))),'data')
    )

    race_data, track_field = jsoner.RaceSaver.load_folder(data_folder)
    if race_data is None or track_field is None:
        sg.popup_error('Error loading data', 'Please choose a correct race data folder')
        exit()  

    view = Viewer(track_field, race_data)
    view.run()