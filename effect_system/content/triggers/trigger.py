from ..event_manager import EventManager
from abc import ABC, abstractmethod


class Trigger(ABC):
    def __init__(self):
        self._event_manager = EventManager()
        self._parent = None
        self._is_armed = False

    def set_parent(self, parent):
        self._parent = parent

    @abstractmethod
    def arm(self):
        self._is_armed = True

    @abstractmethod
    def disarm(self):
        self._is_armed = False

    @abstractmethod
    def update(self, event_data, trigger=None):
        self._parent.update(event_data, trigger=trigger)
