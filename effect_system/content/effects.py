from .event_manager import EventManager
from .triggers import EventTrigger
from abc import ABC, abstractmethod


class Effect(ABC):
    def __init__(self):
        self._trigger = None
        self._targeters = []
        self._event_manager = EventManager()

    def set_trigger(self, trigger, *validators):
        if isinstance(trigger, str):
            self._trigger = EventTrigger(trigger, *validators)
        else:
            self._trigger = trigger
        self._trigger.set_parent(self)
        return self

    def add_targeter(self, targeter):
        self._targeters.append(targeter)
        return self

    def get_targets(self, event_data):
        targets = []
        for targeter in self._targeters:
            targets.extend(targeter.get_targets(event_data))
        return targets

    def arm_trigger(self, should_arm):
        if should_arm:
            self._trigger.arm()
        else:
            self._trigger.disarm()

    def update(self, event_data, trigger=None):
        if self._targeters:
            self.activate_on_targets(event_data)
        else:
            self.activate(event_data, None)

    def activate_on_targets(self, event_data):
        for target in self.get_targets(event_data):
            self.activate(event_data, target)

    @abstractmethod
    def activate(self, event_data, target):
        pass
