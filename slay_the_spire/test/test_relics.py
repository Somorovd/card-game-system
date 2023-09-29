from effect_system import Effect, EventTrigger

from . import *
from ..game.relics import *


@pytest.fixture
def players():
    return [Player("jay"), Player("larry")]


def test_relic_init():
    relic = Relic("test relic")
    assert relic.name == "test relic"
    assert len(relic.stats) == 0
    assert len(relic.effects) == 0


def test_add_effect_to_relic():
    class TestEffect(Effect):
        def activate(self):
            pass

    relic = Relic("test relic")
    effect = TestEffect()
    res = relic.add_effect(effect)

    assert res == relic
    assert len(relic.effects) == 1
    assert relic.effects[0] == effect


def test_relic_effects_active_after_equip():
    class TestEffect(Effect):
        def activate(self):
            pass

    relic = Relic("test relic")
    effect = TestEffect()
    trigger = EventTrigger("event_name")
    relic.add_effect(effect.set_trigger(trigger))
    relic.on_equip()
    assert trigger._is_armed == True


def test_burning_blood(event_manager, game_manager):
    player = game_manager.player
    player.equip_relic(BurningBlood())
    player.take_damage(50, None)
    event_manager.trigger_event("on_combat_end", {})
    assert player.get_stat("health") == 56


def test_akabako(event_manager, players):
    jay, larry = players
    jay.equip_relic(Akabako())

    event_manager.trigger_event("on_combat_start", {})
    jay.attack(larry, 2)
    assert larry.get_stat("health") == 90
    jay.attack(larry, 2)
    assert larry.get_stat("health") == 88
    event_manager.trigger_event("on_combat_start", {})
    jay.attack(larry, 2)
    assert larry.get_stat("health") == 78


def test_bronze_scales(event_manager, game_manager, players):
    jay, larry = players
    jay.equip_relic(BronzeScales())

    game_manager.enemies.append(larry)
    larry.attack(jay, 2)
    assert larry.get_stat("health") == 97
