from .game_manager import GAME_MANAGER
from .statable import Statable, Stat
from .effects import *
from .validators import *
from .targeters import *


class Relic(Statable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.player = None
        self.effects = []
        self.data = {}

    def add_effect(self, event_name, effect):
        self.effects.append(effect)
        effect.on_add_to_relic(self, event_name)
        return self

    def equip_to_player(self, player):
        self.player = player
        for effect in self.effects:
            GAME_MANAGER.add_listener(effect.event_name, effect.update)
            effect.on_equip(player)
