from GameManager import GAME_MANAGER


class Relic:
    # TODO add list of effects that get enabled when attached to a player

    def __init__(self, name):
        self.name = name
        self.player = None
        self.data = {}

    def attach_to(self, player):
        self.player = player

    def add_effect(self, event_name, effect):
        effect.on_add(self)
        GAME_MANAGER.add_listener(event_name, effect.listener)
        return self
