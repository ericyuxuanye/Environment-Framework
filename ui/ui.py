import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import math

import numpy as np
import pygame
from numpy._typing import NDArray
from scipy.interpolate import make_interp_spline

from core.src import jsoner
from core.src.race import ActionCarState, RaceData
from core.src.track import TileType, TrackField
from core.test.samples import Factory

pygame.init()


class UI:
    __slots__ = (
        "screen",
        "width",
        "height",
        "background",
        "race_data",
        "field_width",
        "field_height",
        "width_multiplier",
        "height_mulplier",
        "framerate",
        "interpolation_amount",
        "interpolated_data",
    )

    def __init__(
        self, width: int, height: int, race_data: RaceData, track_field: TrackField, framerate: int = 60, frames_per_entry: int = 1
    ):
        """
        Creates a new UI instance
        """
        self.width = width
        self.height = height
        self.field_height, self.field_width = track_field.field.shape
        self.width_multiplier = self.width / self.field_width
        self.height_mulplier = self.height / self.field_height
        self.screen = pygame.display.set_mode(
            (width, height), flags=pygame.HWSURFACE | pygame.DOUBLEBUF, vsync=1
        )
        self.background = pygame.transform.scale(
            UI.track_field_to_surface(track_field),
            (width, height),
        )
        self.race_data = race_data
        self.interpolation_amount = frames_per_entry
        self.framerate = framerate
        self.interpolated_data = self.interpolate_data(race_data.steps, frames_per_entry)

    @staticmethod
    def interpolate_data(steps: list[ActionCarState], interpolation_amount: int):
        data = np.empty((len(steps), 4), dtype=np.float64)
        for i, entry in enumerate(steps):
            position = entry.car_state.position
            data[i,:2] = position.x, position.y
            if i < len(steps) - 1:
                accel_magnitude = steps[i+1].action.forward_acceleration
                accel_direction = steps[i+1].car_state.wheel_angle
                accel_x = accel_magnitude * math.cos(accel_direction)
                accel_y = accel_magnitude * math.sin(accel_direction)
                data[i, 2:] = accel_x, accel_y
        data[len(steps) - 1, 2:] = data[len(steps) - 2, 2:]
        if interpolation_amount == 1:
            return data
        new_x = np.linspace(0, len(steps) - 1, len(steps) * interpolation_amount)
        return make_interp_spline(np.arange(len(steps)), data)(new_x)


    @staticmethod
    def track_field_to_surface(field: TrackField) -> pygame.Surface:
        tile_type_array: NDArray[np.uint16] = field.field["type"].T
        color_array = np.zeros((*tile_type_array.shape, 3))

        road_mask = tile_type_array == TileType.Road.value
        shoulder_mask = tile_type_array == TileType.Shoulder.value
        wall_mask = tile_type_array == TileType.Wall.value

        # Roads are green
        color_array[road_mask] = (0, 192, 0)
        # shoulders are yellow  
        color_array[shoulder_mask] = (192, 192, 0)
        # walls are red
        color_array[wall_mask] = (192, 0, 0)

        return pygame.surfarray.make_surface(color_array)

    def start(self):
        clock = pygame.time.Clock()
        for state in self.interpolated_data:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            # draw background
            self.screen.blit(self.background, (0, 0))
            # draw car
            car_x = round(state[0] * self.width_multiplier)
            car_y = round(state[1] * self.height_mulplier)

            pygame.draw.circle(
                self.screen,
                "blue",
                (car_x, car_y),
                5,
            )
            # draw acceleration
            accel_x = round(self.width_multiplier * state[2])
            accel_y = round(self.height_mulplier * state[3])
            pygame.draw.line(
                self.screen,
                "green",
                (car_x, car_y),
                (
                    car_x + accel_x,
                    car_y + accel_y
                ),
            )
            pygame.display.flip()
            clock.tick(self.framerate)


if __name__ == "__main__":
    track_field = Factory.sample_track_field_2()
    race_data_saver = jsoner.RaceDataSaver()
    race_data = jsoner.RaceDataSaver.load("data", "SampleRace0_20230512_000000")
    ui = UI(1000, 600, race_data, track_field, 60, 5)
    ui.start()
