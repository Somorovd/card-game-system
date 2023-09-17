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


relic_hawk_eye = Relic("Hawk Eye").add_effect(
    "on_player_add_relic",
    ChangeRelicTiming(-1).add_event_validator(AttachedPlayerValidator().invert()),
)

relic_lion_heart = (
    Relic("Lion Heart")
    .add_effect(
        "on_player_add_relic",
        NTimes(1, StatModifier("max_health", 10))
        .add_targeters(attached_player_targeter)
        .add_event_validator(AttachedPlayerValidator()),
    )
    .add_effect(
        "on_player_add_relic",
        NTimes(1, StatModifier("health", 5))
        .add_targeters(attached_player_targeter)
        .add_event_validator(AttachedPlayerValidator()),
    )
)
