import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from racecar.model import create_model_race
from core.src.jsoner import *


if __name__ == '__main__':

    model, race = create_model_race()
    race.run(debug=False)

    data_root = os.path.join(os.path.dirname(__file__), 'data')
    RaceSaver.save(race, data_root)