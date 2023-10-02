from effect_system.content.triggers import *
from effect_system.content.validators import *
from .validators import *

PlayerTookDamageTrigger = lambda: EventTrigger(
    "on_player_post_take_damage", PropertyInRange("amount", min=1)
)


class OnEquipTrigger(Toggle):
    def __init__(self):
        super().__init__()
        self.set_init_toggled(True)
        self.set_trigger(EventTrigger("on_player_equip_relic"))

    def update(self, event_data, trigger=None):
        print("here")
        super().update(event_data, trigger=trigger)
        if trigger == self._trigger:
            self.disarm()
