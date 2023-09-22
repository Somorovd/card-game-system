from .game_manager import GAME_MANAGER


class Trigger:
    def __init__(self, game_manager=GAME_MANAGER):
        self._game_manager = game_manager


class EventTrigger(Trigger):
    def __init__(self, event_name, *validators, game_manager=GAME_MANAGER):
        super().__init__(game_manager=game_manager)
        self._event_name = event_name
        self._validators = validators
        self._parent = None
        self._is_armed = False

    def set_parent(self, parent):
        self._parent = parent

    def arm(self):
        if self._is_armed:
            return
        self._is_armed = True
        self._game_manager.add_listener(self._event_name, self.update)

    def disarm(self):
        if not self._is_armed:
            return
        self._is_armed = False
        self._game_manager.remove_listener(self._event_name, self.update)

    def validate_event(self, event_data):
        if not self._validators:
            return True
        return all([v.validate(event_data) for v in self._validators])

    def update(self, event_data):
        if self.validate_event(event_data):
            self._parent.update(event_data)
