from abc import ABC, abstractmethod


class EventManager:
    def __init__(self):
        self._listeners = {}

    def add_listener(self, event_name, listener):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
            self._listeners[event_name].append(listener)

    def notify(self, event_name, event_data):
        if not event_name in self._listeners:
            return

        for listener in self._listeners[event_name]:
            if listener.validate(event_data):
                listener.activate(event_data)


class Listener(ABC):
    @abstractmethod
    def activate(self, event_data):
        pass

    @abstractmethod
    def validate(self, event_data):
        pass
