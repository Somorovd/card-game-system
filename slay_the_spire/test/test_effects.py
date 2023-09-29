from effect_system import EventTrigger

from . import *
from ..game.player import Player
from ..game.relics import Relic
from ..game.effects import *

from ..game.targeters import *


def test_heal_effect(event_manager):
    class TestTargeter(Targeter):
        def get_targets(self, event_data):
            return [player]

    player = Player("jay")
    assert TestTargeter().get_targets({})[0] == player

    player.take_damage(50, None)
    heal_effect = Heal(5)
    heal_effect.set_trigger(EventTrigger("event_name")).add_targeter(TestTargeter())
    heal_effect.arm_trigger(True)
    event_manager.trigger_event("event_name", {})
    assert player.get_stat("health") == 55
