import pytest
from game.player import Player


@pytest.fixture
def players():
    return {"jay": Player("jay"), "larry": Player("larry")}


def test_init_players(players):
    assert players["jay"].health == 10
