import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest

from samples import Factory

class RaceTest(unittest.TestCase):

    def test_000_simple(self):
        print('\n===\ntest_000_simple')
        race = Factory.sample_race_0()

        race.run(debug=True)
        #print('race data\n', race.data)


if __name__ == '__main__':
    unittest.main()

