import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))
import math

import numpy as np
import pygame
from numpy._typing import NDArray

from core.src import jsoner
from core.src.race import RaceData
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
    )

    def __init__(
        self, width: int, height: int, race_data: RaceData, track_field: TrackField
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

    @staticmethod
    def track_field_to_surface(field: TrackField) -> pygame.Surface:
        tile_type_array: NDArray[np.uint16] = field.field["type"].T
        color_array = np.zeros((*tile_type_array.shape, 3))

        road_mask = tile_type_array == TileType.Road.value
        shoulder_mask = tile_type_array == TileType.Shoulder.value
        wall_mask = tile_type_array == TileType.Wall.value
        block_mask = tile_type_array == TileType.Block.value

        # Roads are gray
        color_array[road_mask] = (79, 79, 79)
        # shoulders are light gray
        color_array[shoulder_mask] = (163, 163, 163)
        # walls are red
        color_array[wall_mask] = (255, 0, 0)
        # blocks are white
        color_array[block_mask] = (255, 255, 255)

        return pygame.surfarray.make_surface(color_array)

    def start(self):
        clock = pygame.time.Clock()
        for entry in self.race_data.steps:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    break
            # draw background
            self.screen.blit(self.background, (0, 0))
            # draw car
            position = entry.car_state.position
            car_x = round(position.x * self.width_multiplier)
            car_y = round(position.y * self.height_mulplier)

            pygame.draw.circle(
                self.screen,
                "blue",
                (car_x, car_y),
                5,
            )
            # draw acceleration
            action = entry.action
            if action is not None:
                magnitude = action.forward_acceleration
                direction = entry.car_state.wheel_angle
                accel_x = round(self.width_multiplier * magnitude * math.cos(direction))
                accel_y = round(self.height_mulplier * magnitude * math.sin(direction))
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
            clock.tick(10)


if __name__ == "__main__":
    track_field = Factory.sample_track_field_2()
    race_data_saver = jsoner.RaceDataSaver()
    race_data = jsoner.RaceDataSaver.load(
        "data/race/TrackField2Radius2_20230512_000000"
    )
    ui = UI(1000, 600, race_data, track_field)
    ui.start()
