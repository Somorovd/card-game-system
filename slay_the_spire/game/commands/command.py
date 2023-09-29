from abc import ABC, abstractmethod


class Command(ABC):
    @abstractmethod
    def invoke(self, event_data, target):
        pass
