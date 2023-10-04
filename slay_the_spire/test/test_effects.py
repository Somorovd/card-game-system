from effect_system import EventTrigger
from effect_system.content.operations import *

from . import *
from ..game.player import Player
from ..game.relics import Relic
from ..game.effects import *

from ..game.targeters import *


def test_event_data_update(event_manager):
    effect = EventDataUpdate("x", AddOp(3)).set_trigger(EventTrigger("event_name"))
    effect.arm_trigger(True)
    event_data = {"x": 10}
    res = event_manager.trigger_event("event_name", event_data)
    assert res["x"] == 13


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


def test_take_damage_effect(event_manager):
    class TestTargeter(Targeter):
        def get_targets(self, event_data):
            return [player]

    player = Player("jay")
    assert TestTargeter().get_targets({})[0] == player

    damage_effect = TakeDamage(5)
    damage_effect.set_trigger(EventTrigger("event_name")).add_targeter(TestTargeter())
    damage_effect.arm_trigger(True)
    event_manager.trigger_event("event_name", {})
    assert player.get_stat("health") == 95


def test_draw_cards_effect(event_manager):
    class TestTargeter(Targeter):
        def get_targets(self, event_data):
            return [player]

    player = Player("jay")
    assert TestTargeter().get_targets({})[0] == player

    draw_effect = DrawCards(3)
    draw_effect.set_trigger(EventTrigger("event_name")).add_targeter(TestTargeter())
    draw_effect.arm_trigger(True)
    event_manager.trigger_event("event_name", {})
    assert len(player.hand) == 3
