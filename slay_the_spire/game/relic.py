from .statable import Statable, Stat


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
