import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
import math
from src.core import car

from samples import Factory
import json
from src.core.jsoner import *

class JsonTest(unittest.TestCase):

    def test_100_cc(self):
        print('\n===\ntest_100_cc()')

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


    def test_101_cc(self):
        print('\n===\ntest_101_cc()')

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

    def test_102_save(self):
        print('\n===\ntest_102_save()')
        race = Factory.sample_race_0()
        race_data = race.run(debug=False) 
        race_data.race_info.id = 'TrackField2Radius2_20230512_010101'
        RaceDataSaver.save(race_data, 'data/race')

    def test_103_load(self):
        print('\n===\ntest_103_load()')
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


if __name__ == '__main__':
    unittest.main()

