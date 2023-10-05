from . import *
from ..game.player import Player
from ..game.relics import Relic


@pytest.fixture
def players():
    return [Player("jay"), Player("larry")]


def test_player_init(event_manager):
    player = Player("jay")
    assert player.name == "jay"
    assert player.get_stat("health") == 100
    assert player.get_stat("max_health") == 100
    assert player.get_stat("gold") == 0
    assert player.get_stat("energy") == 3
    assert player._event_manager == event_manager
    assert len(player.relics) == 0


def test_player_attack_damage_heal(players):
    jay, larry = players

    jay.take_damage(3, None)
    assert jay.get_stat("health") == 97

    jay.apply_healing(1)
    larry.apply_healing(1)
    assert jay.get_stat("health") == 98
    assert larry.get_stat("health") == 100

    jay.attack(larry, 25)
    assert larry.get_stat("health") == 75


def test_player_healing_events(event_manager, test_listener, players):
    jay, larry = players
    test_listener.create_listener("on_player_pre_heal")
    test_listener.create_listener("on_player_post_heal")

    jay.apply_healing(55)
    assert len(test_listener.events) == 2
    assert test_listener.events[0][0] == "on_player_pre_heal"
    assert test_listener.events[1][0] == "on_player_post_heal"

    pre_heal_data = test_listener.events[0][1]
    assert len(pre_heal_data) == 2
    assert pre_heal_data["player"] == jay
    assert pre_heal_data["amount"] == 55

    post_heal_data = test_listener.events[1][1]
    assert len(post_heal_data) == 3
    assert post_heal_data["player"] == jay
    assert post_heal_data["amount"] == 55
    assert post_heal_data["heal"] == 0


def test_player_damage_events(event_manager, test_listener, players):
    jay, larry = players
    test_listener.create_listener("on_player_pre_take_damage")
    test_listener.create_listener("on_player_post_take_damage")

    jay.take_damage(10, larry)
    assert len(test_listener.events) == 2
    assert test_listener.events[0][0] == "on_player_pre_take_damage"
    assert test_listener.events[1][0] == "on_player_post_take_damage"

    pre_take_damage_data = test_listener.events[0][1]
    assert len(pre_take_damage_data) == 3
    assert pre_take_damage_data["player"] == jay
    assert pre_take_damage_data["source"] == larry
    assert pre_take_damage_data["amount"] == 10

    post_take_damage_data = test_listener.events[1][1]
    assert len(post_take_damage_data) == 3
    assert post_take_damage_data["player"] == jay
    assert post_take_damage_data["source"] == larry
    assert post_take_damage_data["amount"] == 10


def test_player_attack_events(event_manager, test_listener, players):
    jay, larry = players
    test_listener.create_listener("on_player_pre_take_damage")
    test_listener.create_listener("on_player_post_take_damage")
    test_listener.create_listener("on_player_pre_attack")
    test_listener.create_listener("on_player_post_attack")

    jay.attack(larry, 10)
    assert len(test_listener.events) == 4
    assert test_listener.events[0][0] == "on_player_pre_attack"
    assert test_listener.events[1][0] == "on_player_pre_take_damage"
    assert test_listener.events[2][0] == "on_player_post_take_damage"
    assert test_listener.events[3][0] == "on_player_post_attack"

    pre_attack_data = test_listener.events[0][1]
    assert len(pre_attack_data) == 3
    assert pre_attack_data["player"] == jay
    assert pre_attack_data["target"] == larry
    assert pre_attack_data["amount"] == 10

    post_attack_data = test_listener.events[3][1]
    assert len(post_attack_data) == 3
    assert post_attack_data["player"] == jay
    assert post_attack_data["target"] == larry
    assert post_attack_data["amount"] == 10


def test_equip_relic_to_player(test_listener, players):
    from effect_system import Effect, EventTrigger

    jay, larry = players
    test_listener.create_listener("on_player_equip_relic")

    class TestEffect(Effect):
        def activate(self):
            pass

    relic = Relic("test relic")
    effect = TestEffect()
    trigger = EventTrigger("event_name")
    jay.equip_relic(relic.add_effect(effect.set_trigger(trigger)))
    assert len(jay.relics) == 1
    assert jay.relics[0] == relic
    assert len(test_listener.events) == 1
    assert test_listener.events[0][0] == "on_player_equip_relic"
    assert trigger._is_armed == True

    equip_relic_data = test_listener.events[0][1]
    assert len(equip_relic_data) == 2
    assert equip_relic_data["player"] == jay
    assert equip_relic_data["relic"] == relic


def test_player_pay_energy(players):
    jay, larry = players
    jay.pay_energy(1)
    assert jay.get_stat("energy") == 2
    jay.pay_energy(2)
    assert jay.get_stat("energy") == 0
