from effect_system import Targeter

from .game_manager import GameManager


class PlayerTargeter:
    def get_targets(self, event_data):
        return [GameManager().player]


class SelectedEnemyTargeter:
    def get_targets(self, event_data):
        game_manager = GameManager()
        if game_manager.selected_enemy:
            return [game_manager.selected_enemy]
        else:
            return []


player_targeter = PlayerTargeter()
selected_enemy_targeter = SelectedEnemyTargeter()
