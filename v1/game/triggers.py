from .game_manager import GAME_MANAGER


class Trigger:
    def __init__(self, game_manager=GAME_MANAGER):
        self.game_manager = game_manager


class EventTrigger(Trigger):
    def __init__(self, event_name, *validators, game_manager=GAME_MANAGER):
        super().__init__(game_manager=game_manager)
        self.event_name = event_name
        self.validators = validators
        self.parent = None

    def set_parent(self, parent):
        self.parent = parent

    def arm(self):
        self.game_manager.add_listener(self.event_name, self.update)

    def disarm(self):
        self.game_manager.remove_listener(self.event_name, self.update)

    def validate_event(self, event_data):
        if not self.validators:
            return True
        return all([v.validate(event_data) for v in self.validators])

    def update(self, event_name, event_data):
        if self.validate_event(event_data):
            self.parent.update(event_name, event_data)
