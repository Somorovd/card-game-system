from enum import Enum

from .statable import Statable, Stat


class CardType(Enum):
    ATTACK = 1
    SKILL = 2
    POWER = 3
    CURSE = 4


class Card(Statable):
    def __init__(self, name, type, cost):
        super().__init__()
        self.name = name
        self.type = type
        self.add_stat("cost", cost)
        self._effects = []

    def add_effect(self, effect):
        self._effects.append(effect)
        return self

    def add_targeter(self, targeter):
        self._targeters.append(targeter)
        return self

    def play(self):
        for effect in self._effects:
            effect.activate_on_targets({})
