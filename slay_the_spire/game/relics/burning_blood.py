from effect_system import EventTrigger

from .relic import Relic
from ..effects import Heal
from ..targeters import player_targeter

burning_blood = Relic("Burning Blood").add_effect(
    Heal(6).set_trigger(EventTrigger("on_combat_end")).add_targeter(player_targeter)
)
