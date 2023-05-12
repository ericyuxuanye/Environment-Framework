import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

import unittest

from samples import Factory
from src.core.jsoner import Jsoner

class RaceTest(unittest.TestCase):

    def test_000_simple(self):
        print('\n===\ntest_000_simple')
        race = Factory.sample_race_0()

        race.run(debug=False)
        print('race_info:', race.race_info)
        print('race_json:', Jsoner.to_json(race.race_info))

        print('steps:====================')
        for step in race.steps: 
            #print(step)
            print(Jsoner.to_json(step))



        """
        filename = 'data/race/output.txt'
        outfile = open(filename, 'w')
        outfile.writelines([str(i)+'\n' for i in some_list])
        outfile.close()
        """

if __name__ == '__main__':
    unittest.main()

