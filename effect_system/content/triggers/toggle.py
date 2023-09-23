from .trigger import Trigger


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
