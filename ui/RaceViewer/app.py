import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import math
import numpy as np
from scipy.interpolate import make_interp_spline    
import PySimpleGUI as sg

from core.src import jsoner, car
from core.src.race import ActionCarState, RaceData
from core.src.track import TileType, TrackField
from core.test.samples import Factory

class CarElement:
    def __init__(self, graph, scale):
        self.graph = graph
        self.scale = scale
        self.radius = scale/2

    def show_step(self, step_data):
        position_x = step_data[0]
        position_y = step_data[1]
        angle = step_data[2]


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
        position_x = step_data[0]
        position_y = step_data[1]
        angle = step_data[2]

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
        self.init_components()
        self.steps_data = self.interpolate_data()


    def run(self):
        if (self.steps_data.size > 0):
            self.car_element.show_step(self.steps_data[0])
        
        at:int = 0

        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break

            if event == 'Step':
                at += 1
                if at < self.steps_data.shape[0]:
                    self.car_element.move_to(self.steps_data[at])

        self.window.close()


    def init_config(self):
        self.window_width = 800           
        self.window_height = 600	
        self.scale = 20
        self.step_rate = 1
        
        self.road_color = 'green'
        self.shoulder_color = 'yellow'
        self.wall_color = 'red'


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
        

        self.layout = [
            [sg.Text('Spartabots', justification='center', expand_x=True, text_color='white', font=('Helvetica', 25))],
            [self.graph],
            [sg.Button('Step'), sg.Exit()],
            ]
        
        self.window = sg.Window('Track Field', self.layout, grab_anywhere=True, finalize=True)
        self.draw_track_field()

        self.car_element = CarElement(self.graph, self.scale)
        #self.car_element.show(self.race_data.race_info.start_state)


    def draw_track_field(self):
        for y in range(self.track_field.track_info.row) :
            for x in range(self.track_field.track_info.column) :
                if self.track_field.field[y, x]['type'] == TileType.Wall.value:
                    tile_color = self.wall_color
                elif self.track_field.field[y, x]['type'] == TileType.Road.value:
                    tile_color = self.road_color
                elif self.track_field.field[y, x]['type'] == TileType.Shoulder.value:
                    tile_color = self.shoulder_color

                self.graph.DrawRectangle(
                    (x * self.scale, y * self.scale), 
                    (x * self.scale + self.scale, y * self.scale + self.scale), 
                    fill_color = tile_color, 
                    line_color = tile_color, 
                    line_width = 0)


    def interpolate_data(self):
        steps = self.race_data.steps
        data = np.empty((len(steps), 5))
        for i, entry in enumerate(steps):
            data[i,:3] = entry.car_state.position.x, entry.car_state.position.y, entry.car_state.wheel_angle
            if entry.action is None:
                data[i,3:] = 0, 0
            else:
                data[i,3:] = entry.action.forward_acceleration, entry.action.angular_velocity

        if self.step_rate == 1:
            return data
        
        new_data = np.linspace(0, len(steps) - 1, len(steps) * self.step_rate)
        return make_interp_spline(np.arange(len(steps)), data)(new_data)
    

if __name__ == "__main__":
    track_field = Factory.sample_track_field_2()
    race_data_saver = jsoner.RaceDataSaver()
    race_data = jsoner.RaceDataSaver.load(
        "data/race/TrackField2Radius2_20230512_000000"
    )
    view = Viewer(track_field, race_data)
    view.run()