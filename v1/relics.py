from GameManager import GAME_MANAGER
from effects import *


class Relic:
    def __init__(self, name):
        self.name = name
        self._player = None
        self.effects = []
        self.data = {}

    def add_effect(self, event_name, effect):
        self.effects.append(effect)
        effect.on_add(self)
        GAME_MANAGER.add_listener(event_name, effect)
        return self

    @property
    def player(self):
        return self._player

    def equip_to_player(self, player):
        self._player = player
        for effect in self.effects:
            effect.on_equip(player)


relic_frog_legs = Relic("Frog Legs").add_effect(
    "on_player_pre_heal", IncreaseHealing(4)
)

relic_blood_leech = (
    Relic("Blood Leech")
    .add_effect("on_player_pre_heal", LeechReduce(2))
    .add_effect("on_player_post_heal", LeechHeal(2))
)

relic_tiger_claw = Relic("Tiger Claw").add_effect(
    "on_player_pre_attack", CounterChangeAmount("damage", 5, 3)
)

relic_hawk_eye = Relic("Hawk Eye").add_effect(
    "on_player_add_relic", ChangeRelicTiming(-1)
)
