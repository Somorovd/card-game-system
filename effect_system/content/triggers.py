from .event_manager import EventManager
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


class Sequence(Trigger):
    def __init__(self):
        super().__init__()
        self._triggers = []
        self._reset = None
        self._pos = 0

    def __len__(self):
        return len(self._triggers)

    def arm(self):
        self._is_armed = True
        self._reset.arm()
        self._triggers[self._pos].arm()

    def disarm(self):
        self._is_armed = False
        self._reset.disarm()
        self._triggers[self._pos].disarm()

    def update(self, event_data, trigger=None):
        if self._pos == len(self._triggers) - 1 and self._parent:
            self._parent.update(event_data, trigger=self)

        self._triggers[self._pos].disarm()
        if trigger and trigger == self._reset:
            self._pos = 0
        else:
            self._pos = (self._pos + 1) % len(self._triggers)
        self._triggers[self._pos].arm()

    def add_seq(self, trigger):
        self._triggers.append(trigger)
        trigger.set_parent(self)
        return self

    def add_reset(self, trigger):
        self._reset = trigger
        trigger.set_parent(self)
        return self


class Toggle(Trigger):
    def __init__(self):
        super().__init__()
        self._toggled = False
        self._toggle_on = None
        self._toggle_off = None
        self._trigger = None

    def arm(self):
        self._is_armed = True
        if not self._toggled:
            self._toggle_on and self._toggle_on.arm()
        else:
            self._toggle_off and self._toggle_off.arm()
            self._trigger and self._trigger.arm()

    def disarm(self):
        self._is_armed = False
        if not self._toggled:
            self._toggle_on and self._toggle_on.disarm()
        else:
            self._toggle_off and self._toggle_off.disarm()
        self._trigger and self._trigger.disarm()

    def update(self, event_data, trigger=None):
        if not trigger:
            return
        elif trigger == self._trigger:
            self._parent.update(event_data, trigger=self)
        elif trigger == self._toggle_on:
            self.set_toggled(True)
        elif trigger == self._toggle_off:
            self.set_toggled(False)

    def set_toggled(self, toggled):
        if self._is_armed:
            if toggled and not self._toggled:
                self._toggle_on and self._toggle_on.disarm()
                self._toggle_off and self._toggle_off.arm()
                self._trigger and self._trigger.arm()
            elif not toggled and self._toggled:
                self._toggle_off and self._toggle_off.disarm()
                self._trigger and self._trigger.disarm()
                self._toggle_on and self._toggle_on.arm()
        self._toggled = toggled

    def set_toggle_on(self, trigger):
        self._toggle_on = trigger
        trigger.set_parent(self)

    def set_toggle_off(self, trigger):
        self._toggle_off = trigger
        trigger.set_parent(self)

    def set_trigger(self, trigger):
        self._trigger = trigger
        trigger.set_parent(self)
