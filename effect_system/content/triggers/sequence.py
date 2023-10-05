from .trigger import Trigger


class Sequence(Trigger):
    def __init__(self):
        super().__init__()
        self._triggers = []
        self._restart_trigger = None
        self._pos = 0

    def __len__(self):
        return len(self._triggers)

    def arm(self):
        self._is_armed = True
        self._restart_trigger.arm()
        self._triggers[self._pos].arm()

    def disarm(self):
        self._is_armed = False
        self._restart_trigger.disarm()
        self._triggers[self._pos].disarm()

    def reset(self):
        self.disarm()
        self._pos = 0
        for t in self._triggers:
            t.reset()

    def update(self, event_data, trigger=None):
        if trigger and trigger == self._restart_trigger:
            self._triggers[self._pos].reset()
            self._pos = 0
            self._triggers[self._pos].arm()
            return

        if self._pos == len(self._triggers) - 1 and self._parent:
            self._parent.update(event_data, trigger=self)

        self._triggers[self._pos].reset()
        self._pos = (self._pos + 1) % len(self._triggers)
        self._triggers[self._pos].arm()

    def add_seq(self, trigger):
        self._triggers.append(trigger)
        trigger.set_parent(self)
        return self

    def add_restart(self, trigger):
        self._restart_trigger = trigger
        trigger.set_parent(self)
        return self
