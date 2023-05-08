import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest
import math
from src.core import race
from race_sample import RaceSample

class RaceTest(unittest.TestCase):

    def test_000_simple(self):
        print('\n===\ntest_000_simple')
        race = RaceSample.sample_race_0()

        race.run()
        print('race data\n', race.data)

if __name__ == '__main__':
    unittest.main()

