import pytest
from game import *


@pytest.fixture
def players():
    jay = Player("Jay")
    jay.stats["health"] = Stat(10)
    jay.stats["max_health"] = Stat(100)
    larry = Player("Larry")
    larry.stats["health"] = Stat(10)
    larry.stats["max_health"] = Stat(100)
    return {"jay": jay, "larry": larry}


def test_player_healing(players):
    """Testing a players ability to heal"""
    jay = players["jay"]
    larry = players["larry"]

    # confirm that event data is not altered
    pre_heal_amount = 1
    pre_heal_event_data = {"player": jay, "amount": pre_heal_amount}
    res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
    assert res["amount"] == pre_heal_amount

    # confirm player health after healing
    jay.apply_healing(2)
    assert jay.health == 12
    assert larry.health == 10
    larry.apply_healing(25)
    assert jay.health == 12
    assert larry.health == 35
    larry.apply_healing(100)
    assert larry.health == 100


def test_increase_attached_player_healing_relic(players):
    """Testing a relic that increases the amount a player heals"""
    heal_increase = 4
    relic_frog_legs = Relic("Frog Legs").add_effect(
        "on_player_pre_heal",
        EventDataUpdate("amount", heal_increase).add_event_validator(
            AttachedPlayerValidator()
        ),
    )
    jay = players["jay"]
    larry = players["larry"]

    jay.add_relic(relic_frog_legs)

    # confirm that event data is altered
    pre_heal_amount = 1
    pre_heal_event_data = {"player": jay, "amount": pre_heal_amount}
    res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
    assert res["amount"] == pre_heal_amount + heal_increase

    # confirm resulting player health
    health = jay.health
    heal_amount1 = 2
    heal_amount2 = 10
    jay.apply_healing(heal_amount1)
    assert jay.health == health + heal_amount1 + heal_increase
    health = jay.health
    jay.apply_healing(heal_amount2)
    assert jay.health == health + heal_amount2 + heal_increase

    # confirm no effect on other players
    assert larry.health == 10
    health = jay.health
    larry.apply_healing(4)
    assert larry.health == 14
    assert jay.health == health
