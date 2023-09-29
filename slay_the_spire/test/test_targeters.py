from . import *

from ..game.game_manager import GameManager
from ..game.targeters import *


def test_player_targeter(game_manager):
    from ..game.player import Player

    player = Player("jay")
    game_manager.player = player
    targeter = player_targeter
    targets = targeter.get_targets({})
    assert len(targets) == 1
    assert targets[0] == player
