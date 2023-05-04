
import unittest 
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
from src.core.car import *

class SimpleTest(unittest.TestCase):

    def test_1(self):
        t = Point2D(3, 5)
        print(t)
        self.assertTrue(t.x == 3)
        self.assertTrue(t.y == 5)


if __name__ == '__main__':
    unittest.main()

