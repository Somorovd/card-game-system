import pytest
from game import *


@pytest.fixture
def players():
    return {"jay": Player("jay"), "larry": Player("larry")}


def test_increase_healing_relic(players):
    """Testing a relic that increases the amount a player heals"""
    heal_increase = 4
    relic_frog_legs = Relic("Frog Legs").add_effect(
        "on_player_pre_heal",
        EventDataUpdate("amount", heal_increase).add_validator(
            AttachedPlayerValidator()
        ),
    )

    # confirm starting health
    jay = players["jay"]
    assert jay.health == 10

    # confirm that event data is not altered
    pre_heal_amount = 1
    pre_heal_event_data = {"player": jay, "amount": pre_heal_amount}
    res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
    assert res["amount"] == pre_heal_amount

    # confirm resulting player health
    jay.apply_healing(2)
    assert jay.health == 12

    # add testing relic
    jay.add_relic(relic_frog_legs)

    # confirm that event data is altered
    pre_heal_amount = 1
    pre_heal_event_data = {"player": jay, "amount": pre_heal_amount}
    res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
    assert res["amount"] == pre_heal_amount + heal_increase

    # confirm resulting player health
    jay.apply_healing(2)
    assert jay.health == 18
    jay.apply_healing(10)
    assert jay.health == 32

    # confirm no effect when other players heal
    larry = players["larry"]
    assert larry.health == 10
    larry.apply_healing(4)
    assert larry.health == 14
    assert jay.health == 32
