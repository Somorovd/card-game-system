from abc import ABC, abstractmethod


class Targeter(ABC):
    @abstractmethod
    def get_targets(self, event_data):
        pass


class EventDataTargeter(Targeter):
    def get_targets(self, event_data):
        return [event_data]


class EventDataPropertyTargeter(Targeter):
    def __init__(self, data_type):
        self.data_type = data_type

    # what if the property is an array already?
    def get_targets(self, event_data):
        if not self.data_type in event_data:
            return []
        prop = event_data[self.data_type]
        if isinstance(prop, list):
            return prop
        else:
            return [prop]


event_data_targeter = EventDataTargeter()
