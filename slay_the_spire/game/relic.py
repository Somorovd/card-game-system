# from .event_manager import EVENT_MANAGER
from .statable import Statable, Stat
# from .effects import *
# from .validators import *
# from .targeters import *


class Relic(Statable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.effects = []

    def add_effect(self, effect):
        self.effects.append(effect)
        return self

    def on_equip(self):
        for effect in self.effects:
            effect.arm_trigger(True)

#     def equip_to_player(self, player):
#         self.player = player
#         for effect in self.effects:
#             EVENT_MANAGER.add_listener(effect.event_name, effect.update)
#             effect.on_equip(player)
