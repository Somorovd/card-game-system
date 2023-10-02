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

    karen = Player("karen")
    jay.take_damage(7, karen)
    assert karen.get_stat("health") == 100


def test_ring_of_the_snake(event_manager, game_manager, players):
    jay, larry = players
    jay.equip_relic(RingOfTheSnake())

    jay.draw_cards(1)
    assert len(jay.hand) == 1

    event_manager.trigger_event("on_combat_start", {})
    jay.draw_cards(1)
    assert len(jay.hand) == 4

    jay.draw_cards(1)
    assert len(jay.hand) == 5

    event_manager.trigger_event("on_combat_start", {})
    jay.draw_cards(1)
    assert len(jay.hand) == 8


def test_centennial_puzzle(event_manager, game_manager, players):
    jay, larry = players
    game_manager.player = jay
    jay.equip_relic(CentennialPuzzle())

    larry.attack(jay, 4)
    assert len(jay.hand) == 0

    event_manager.trigger_event("on_combat_start", {})
    larry.attack(jay, 0)
    assert len(jay.hand) == 0

    larry.attack(jay, 2)
    assert len(jay.hand) == 3

    larry.attack(jay, 2)
    assert len(jay.hand) == 3

    event_manager.trigger_event("on_combat_start", {})
    larry.attack(jay, 2)
    assert len(jay.hand) == 6


def test_maw_bank(event_manager, game_manager, players):
    jay, larry = players
    game_manager.player = jay
    jay.equip_relic(MawBank())

    event_manager.trigger_event("on_player_climb_floor", {})
    assert jay.get_stat("gold") == 12

    event_manager.trigger_event("on_player_climb_floor", {})
    event_manager.trigger_event("on_player_climb_floor", {})
    assert jay.get_stat("gold") == 36

    event_manager.trigger_event("on_player_shop_purchase", {})
    event_manager.trigger_event("on_player_climb_floor", {})
    assert jay.get_stat("gold") == 36
