import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest 
from car_test import CarTest
from track_test import TrackTest
from race_test import RaceTest
from jsoner_test import JsonTest

if __name__ == '__main__':
    unittest.main()

