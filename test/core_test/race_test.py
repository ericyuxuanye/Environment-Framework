import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest

from samples import Factory
from src.core.race import ActionCarState, Race
from src.core.jsoner import *

class RaceTest(unittest.TestCase):

    def ttest_000_simple(self):
        print('\n===\ntest_000_simple')
        race = Factory.sample_race_0()

        race.run(debug=False)

        directory = os.path.join('data/race', )
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

        

    def test_001_readback(self):
        info_path = 'data/race/TrackField2Radius2_20230511_221852/info.json'
        race_info_read = Jsoner.object_from_json_file(info_path)
        print('race_info_read : ', race_info_read)

        steps: list[ActionCarState] = []
        log_path = 'data/race/TrackField2Radius2_20230511_221852/action_state.log'
        with open(log_path, 'r') as logfile:
            Lines = logfile.readlines()
        
            for line in Lines:
                steps.append(Jsoner.from_json_str(line))

        print('steps: ', steps)


    def test_100_simple(self):
        print('\n===\ntest_100_simple')
        race = Factory.sample_race_0()
        race_data = race.run(debug=False) 
        race_data.race_info.id = 'TrackField2Radius2_20230512_000000'
        RaceDataSaver.save(race_data, 'data/race')

    def test_101_readback(self):
        info_path = 'data/race/TrackField2Radius2_20230512_000000'
        race_data = RaceDataSaver.load(info_path)
        print('race_data : ', race_data)

if __name__ == '__main__':
    unittest.main()

