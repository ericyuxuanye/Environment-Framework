from abc import ABC, abstractmethod
from . import car
from . import track


class IModelLoad(ABC):
    @abstractmethod
    def load(self, folder:str) -> bool:
        """
        Loads the model from a folder
        """
        raise NotImplementedError
    

class IModelSave(ABC):
    @abstractmethod
    def save(self, folder:str) -> bool:
        """
        Saves the model into a folder
        """
        raise NotImplementedError


class IModelInference(IModelLoad):
    @abstractmethod
    def get_action(self, car_state: car.CarState, car_view: track.CarView) -> car.Action:
        """
        Returns the appropriate action given car state and visible track view
        """
        raise NotImplementedError


class IModelTrainOnline(IModelLoad, IModelSave):
    def update_online(self, start: car.CarState, action: car.Action, end: car.CarState) -> bool:
        """
        for each interaction (state, action) -> next_state
        """
        raise NotImplementedError


class IModelTrainOffline(IModelLoad, IModelSave):
    pass

    """
    def update_offline(self, dataset: RaceDataset) -> bool:

        For offline training, tun with dataset from a complete race

        raise NotImplementedError
    """
