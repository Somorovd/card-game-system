from effect_system import Targeter

from .game_manager import GameManager


class PlayerTargeter:
    def get_targets(self, event_data):
        return [GameManager().player]


player_targeter = PlayerTargeter()
