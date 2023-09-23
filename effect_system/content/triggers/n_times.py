from .toggle import Toggle


class NTimes(Toggle):
    def __init__(self, trigger, max_count):
        super().__init__()
        self._trigger = trigger
        trigger.set_parent(self)
        self._max_count = max_count
        self._count = 0
        self.set_init_toggled(True)

    def update(self, event_data, trigger=None):
        if self._count < self._max_count:
            super().update(event_data, trigger)
            self._count += 1
        if self._count >= self._max_count:
            self.disarm()

    def reset(self):
        super().reset()
        self._count = 0
