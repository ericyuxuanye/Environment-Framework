import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import unittest
import math

from samples import Factory
from src import car
from src.jsoner import *

class JsonTest(unittest.TestCase):

    def test_100_carconfig_json(self):
        print('\n===\ntest_100_carconfig_json()')

        cc_1= Factory.default_car_config()
        print('cc_1:', cc_1)
        print('type(cc_1):', type(cc_1))

        cc_json = Jsoner.to_json(cc_1)
        print('cc_json:', cc_json)

        cc_2 = json.loads(cc_json)
        print('cc_2:', cc_2)
        print('type(cc_2):', type(cc_2))

        cc_3 = Jsoner.from_json_dict(cc_2)
        print('cc_3:', cc_3)
        print('type(cc_3):', type(cc_3))

        print('cc_1 == cc_3:', cc_1 == cc_3) 


    def test_101_carconfig_folder(self):
        print('\n===\ntest_101_carconfig_folder()')

        cc_1= Factory.default_car_config()
        print('cc_1:', cc_1)
        print('type(cc_1):', type(cc_1))

        directory = 'data/carconfig'
        if not os.path.exists(directory):
            os.makedirs(directory)

        file_name = 'data/carconfig/cc_1.json'
        Jsoner.to_json_file(cc_1, file_name)

        cc_2 = Jsoner.dict_from_json_file(file_name)
        print('cc_2:', cc_2)
        print('type(cc_2):', type(cc_2))

        cc_3 = Jsoner.object_from_json_file(file_name)
        print('cc_3:', cc_3)
        print('type(cc_3):', type(cc_3))

        print('cc_1 == cc_3:', cc_1 == cc_3) 


    def test_102_save_racedata(self):
        print('\n===\ntest_102_save_racedata()')
        race = Factory.sample_race_0()
        race_data = race.run(debug=False) 
        race_data.race_info.id = 'TrackField2Radius2_20230512_010101'
        RaceDataSaver.save(race_data)


    def test_103_load_racedata(self):
        print('\n===\ntest_103_load_racedata()')
        info_path = 'data/race/TrackField2Radius2_20230512_010101'
        race_data = RaceDataSaver.load(info_path)
        print('race_data : ', race_data)

    def test_400_save_tf(self):
        print('\n===\ntest_400_save_tf()')

        tf = Factory.sample_track_field_0()
        print('tf:', tf)
        print('type(tf):', type(tf))

        TrackFieldSaver.save(tf, 'data/trackfield')

    def test_401_load_tf(self):
        print('\n===\ntest_401_load_tf()')
        tf_path = 'data/trackfield/sample_track_field_0'
        tf= TrackFieldSaver.load(tf_path)
        print('tf : ', tf)


    def test_500_save_race(self):
        print('\n===\nttest_100_save()')
        race = Factory.sample_race_0()
        race_data = race.run(debug=False) 
        race_data.race_info.id = 'TrackField2Radius2_20230512_000000'

        RaceSaver.save(race)

        """

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
        
        """


    def test_501_read_race(self):
        print('\n===\ntest_501_read_race()')

        track_field, race_data = RaceSaver.load('data', 'TrackField2Radius2_20230512_000000')
        """
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
        """


        print('track_field: \n', track_field)
        print('race_data: \n', race_data)
        

if __name__ == '__main__':
    unittest.main()

