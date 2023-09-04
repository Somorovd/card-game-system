from EventManager import EventManager


class GameManager:
    def __init__(self):
        self._event_manager = EventManager()

    def add_listener(self, event_name, listener):
        self._event_manager.add_listener(event_name, listener)

    def remove_listener(self, event_name, listener):
        self._event_manager.remove_listener(event_name, listener)

    def trigger_event(self, event_name, event_data):
        data_copy = event_data.copy()
        self._event_manager.notify(event_name, data_copy)
        return data_copy


GAME_MANAGER = GameManager()
