import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import math    
import PySimpleGUI as sg

from core.src import jsoner
from core.src.race import ActionCarState, RaceData
from core.src.track import TileType, TrackField
from core.test.samples import Factory


class Viewer:
    def __init__(self,  track_field: TrackField):
        self.track_field = track_field

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
        self.tile_size = 20
        
        self.road_color = 'green'
        self.shoulder_color = 'yellow'
        self.wall_color = 'red'


    def init_components(self):
        track_info = self.track_field.track_info

        field_width, field_height = track_info.column * self.tile_size, track_info.row * self.tile_size
        self.graph = sg.Graph(
            canvas_size=(field_width, field_height), 
            graph_bottom_left=(0, field_height), 
            graph_top_right=(field_width, 0), 
            background_color='white', 
            key='graph', 
            tooltip='track field')
        

        self.layout = [
            [sg.Text('Track Field')],
            [self.graph],
            [sg.Button('Read'), sg.Exit()],
            ]
        
        self.window = sg.Window('Track Field', self.layout, grab_anywhere=True, finalize=True)
        self.draw_track_field()

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
                    (x * self.tile_size, y * self.tile_size), 
                    (x * self.tile_size + self.tile_size, y * self.tile_size + self.tile_size), 
                    fill_color = tile_color, 
                    line_color = tile_color, 
                    line_width = 0)
                    

if __name__ == "__main__":
    track_field = Factory.sample_track_field_2()
    race_data_saver = jsoner.RaceDataSaver()
    race_data = jsoner.RaceDataSaver.load(
        "data/race/TrackField2Radius2_20230512_000000"
    )
    view = Viewer(track_field)
    view.run()