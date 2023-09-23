from .trigger import Trigger


class EventTrigger(Trigger):
    def __init__(self, event_name, *validators):
        super().__init__()
        self._event_name = event_name
        self._validators = validators

    def arm(self):
        if self._is_armed:
            return
        self._is_armed = True
        self._event_manager.add_listener(self._event_name, self.update)

    def disarm(self):
        if not self._is_armed:
            return
        self._is_armed = False
        self._event_manager.remove_listener(self._event_name, self.update)

    def validate_event(self, event_data):
        if not self._validators:
            return True
        return all([v.validate(event_data) for v in self._validators])

    def update(self, event_data, trigger=None):
        if self.validate_event(event_data) and self._parent:
            self._parent.update(event_data, trigger=self)
