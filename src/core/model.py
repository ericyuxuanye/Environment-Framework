from dataclasses import dataclass
from abc import ABC, abstractmethod
from car import CarState
from race import RaceDataset


@dataclass
class Action:
    __slots__ = ["linear_acceleration", "angular_velocity"]

    linear_acceleration: float
    """The linear acceleration of the car in the direction of the wheel"""

    angular_velocity: float


class IModel(ABC):
    @abstractmethod
    def load(self) -> bool:
        """
        Loads the model from a saved file
        """
        raise NotImplementedError

    @abstractmethod
    def save(self) -> bool:
        """
        Saves the model to a file
        """
        raise NotImplementedError

    @abstractmethod
    def get_action(self, state: CarState) -> Action:
        """
        Returns the appropriate action given the state
        """
        raise NotImplementedError

    def update_online(self, new_state: CarState) -> bool:
        """
        Should be called right after the environment
        performed the action. This method should calculate
        the reward and update the model parameters in order
        to maximize the reward.

        This method specifically is for online training
        """
        raise NotImplementedError

    def update_offline(self, dataset: RaceDataset) -> bool:
        """
        Should be called right after the environment
        performed the action. This method should calculate
        the reward and update the model parameters in order
        to maximize the reward.

        For offline training
        """
        raise NotImplementedError