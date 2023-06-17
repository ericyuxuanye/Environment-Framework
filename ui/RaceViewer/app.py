import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import math    
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

    def show(self, car_state: car.CarState):
        self.circle_figure = self.graph.DrawCircle(
            [car_state.position.x * self.scale, car_state.position.y * self.scale], 
            self.radius, 
            fill_color='blue', 
            line_color='blue'
        )

        angle_x = math.cos(car_state.wheel_angle) + car_state.position.x
        angle_y = math.sin(car_state.wheel_angle) + car_state.position.y
        self.angle_figure = self.graph.DrawLine(
            [car_state.position.x * self.scale, car_state.position.y * self.scale],
            [angle_x * self.scale, angle_y * self.scale],
            color = 'white', 
            width = 2
        )

        velocity_x = car_state.velocity_x + car_state.position.x
        velocity_y = car_state.velocity_y + car_state.position.y
        self.velocity_figure = self.graph.DrawLine(
            [car_state.position.x * self.scale, car_state.position.y * self.scale],
            [velocity_x * self.scale, velocity_y * self.scale],
            color = 'orange', 
            width = 2
        )

    def move_to(self, car_state: car.CarState):
        pass


class Viewer:
    def __init__(self,  track_field: TrackField, race_data: RaceData):
        self.track_field = track_field
        self.race_data = race_data

        self.init_config()
        self.init_components()


    def run(self):
        while True:
            event, values = self.window.read()
            if event == sg.WIN_CLOSED or event == 'Exit':
                break
        self.window.close()


    def init_config(self):
        self.window_width = 800           
        self.window_height = 600	
        self.scale = 20
        
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
            [sg.Button('Start'), sg.Exit()],
            ]
        
        self.window = sg.Window('Track Field', self.layout, grab_anywhere=True, finalize=True)
        self.draw_track_field()

        self.car_element = CarElement(self.graph, self.scale)
        self.car_element.show(self.race_data.race_info.start_state)

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
                    

if __name__ == "__main__":
    track_field = Factory.sample_track_field_2()
    race_data_saver = jsoner.RaceDataSaver()
    race_data = jsoner.RaceDataSaver.load(
        "data/race/TrackField2Radius2_20230512_000000"
    )
    view = Viewer(track_field, race_data)
    view.run()