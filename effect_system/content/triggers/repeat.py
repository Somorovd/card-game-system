from .trigger import Trigger


class Repeat(Trigger):
    def __init__(self, max_count, trigger):
        super().__init__()
        self._max_count = max_count
        self._count = 0
        self._trigger = trigger
        trigger.set_parent(self)

    def arm(self):
        self._is_armed = True
        self._trigger.arm()

    def disarm(self):
        self._is_armed = False
        self._trigger.disarm()

    def reset(self):
        self.disarm()
        self._count = 0

    def update(self, event_data, trigger=None):
        self._count += 1
        if self._count == self._max_count:
            self._parent.update(event_data, trigger=trigger)
            self._count = 0
