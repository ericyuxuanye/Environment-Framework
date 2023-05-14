import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
import math
from src.core import car

from samples import Factory
import json
from src.core.jsoner import Jsoner

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

    
    def test_200_tf(self):
        print('\n===\ntest_200_tf()')

        tf_1= Factory.sample_track_field_0()
        print('tf0:', tf_1)
        print('type(tf0):', type(tf_1))


if __name__ == '__main__':
    unittest.main()

