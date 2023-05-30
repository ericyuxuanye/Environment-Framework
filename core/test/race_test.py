import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
import math

from samples import Factory
from src.race import ActionCarState, Race
from src.jsoner import *

class RaceTest(unittest.TestCase):

    def test_000_simple(self):
        print('\n===\ntest_000_simple()')
        race = Factory.sample_race_0()
        # print('track:\r', race.race_info.track_info)

        race.run(debug=True)


    def test_001_back(self):
        print('\n===\ntest_001_back()')
        race = Factory.sample_race_0()
        race.race_info.start_state = CarState(position = Point2D(y = 5.5, x = 14.5), wheel_angle=3.14)
        print('track:\r', race.race_info.track_info)
        self.assertTrue(race.race_info.track_info.round_distance == 28)

        race.run(debug=True)
        self.assertTrue(race.steps[-1].car_state.round_count == -1)
        self.assertTrue(race.steps[-1].car_state.track_state.last_road_tile_total_distance < 0)


    def test_100_save(self):
        print('\n===\nttest_100_save()')
        race = Factory.sample_race_0()
        race_data = race.run(debug=False) 
        race_data.race_info.id = 'TrackField2Radius2_20230512_000000'

        directory = os.path.join('data/race', race_data.race_info.id)
        if not os.path.exists(directory):
            os.makedirs(directory)
        
        info_file = 'info.json'
        info_path = os.path.join(directory, info_file)
        with open(info_path, 'w') as infofile:
            info_json = Jsoner.to_json(race.race_info, indent=4)
            print('race_json', info_json)
            infofile.write(info_json)


        print('steps:====================')
        step_path = os.path.join(directory, 'action_state.log')
        with open(step_path, 'w') as logfile:
            for step in race.steps: 
                step_json = Jsoner.to_json(step)
                print(step_json)
                logfile.write(step_json + '\n')


    def test_101_readback(self):
        print('\n===\ntest_101_readback()')

        directory = os.path.join('data/race/', 'TrackField2Radius2_20230512_000000')
        info_path = os.path.join(directory, 'info.json')
        race_info_read = Jsoner.object_from_json_file(info_path)
        print('race_info_read : ', race_info_read)

        steps: list[ActionCarState] = []
        log_path = os.path.join(directory, 'action_state.log')
        with open(log_path, 'r') as logfile:
            Lines = logfile.readlines()
        
            for line in Lines:
                steps.append(Jsoner.from_json_str(line))

        print('steps: ', steps)


    def test_200_too_low_power(self):
        print('\n===\ntest_400_too_low_power')

        race = Factory.sample_race_0()
        
        low_power_action = car.Action(1,0)
        print('low_power_action = ', low_power_action)
        state_1 = race.track_field.get_next_state(
            car_config=race.race_info.car_config, 
            car_state=race.race_info.start_state, 
            action=low_power_action)
        print('state_1 = ', state_1)
        self.assertTrue(state_1.velocity_x == 0)
        self.assertTrue(state_1.velocity_y == 0)
        self.assertTrue(state_1.wheel_angle == 0)
        self.assertTrue(state_1.timestamp == race.race_info.track_info.time_interval)

if __name__ == '__main__':
    unittest.main()

