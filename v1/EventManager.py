class EventManager:
    def __init__(self):
        self._listeners = {}

    def add_listener(self, event_name, listener):
        if event_name not in self._listeners:
            self._listeners[event_name] = []
        self._listeners[event_name].append(listener)

    def notify(self, event_name, event_data):
        if event_name in self._listeners:
            for listener in self._listeners[event_name]:
                listener(event_data)
