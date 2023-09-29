from effect_system.content.triggers import *
from effect_system.content.validators import *
from .validators import *

PlayerTookDamageTrigger = lambda: EventTrigger(
    "on_player_post_take_damage", PropertyInRange("amount", min=1)
)
