from data import CarView, CarState, Action, TrackField, CarConfig, TileConfig
from abc import ABC, abstractmethod


class TrackSystem(ABC):
    __slots__ = ["track_field"]
    """
    The track field storing information about the track
    """
    track_field: TrackField

    @abstractmethod
    def get_car_view(self, state: CarState) -> CarView:
        """
        Returns the view of the car given the state
        """
        raise NotImplementedError

    @abstractmethod
    def get_next_state(self, state: CarState, action: Action) -> CarState:
        """
        Returns the next state of the car after performing action
        """
        raise NotImplementedError

    def get_field_shape(self):
        """
        Returns the shape of the track field (width, height)
        """
        return self.track_field.field.shape

    @abstractmethod
    def _get_next_state(
        self,
        state: CarState,
        action: Action,
        time_interval: float,
        car_config: CarConfig,
        tile_config: TileConfig,
    ):
        """
        The private method that implements the physics engine. This should be stable
        """
        raise NotImplementedError
