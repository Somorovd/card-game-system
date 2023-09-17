from abc import ABC, abstractmethod


class Targeter(ABC):
    @abstractmethod
    def get_targets(self, effect, event_data):
        pass


class EventDataTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return [event_data]


class EventDataPropertyTargeter(Targeter):
    def __init__(self, data_type):
        self.data_type = data_type

    # what if the property is an array already?
    def get_targets(self, effect, event_data):
        return [event_data[self.data_type]]


class AttachedPlayerTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return [effect.relic.player]


class AttachedPlayerRelicsTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return effect.relic.player.relics


class AttachedRelicTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return [effect.relic]


event_data_targeter = EventDataTargeter()
attached_player_targeter = AttachedPlayerTargeter()
attached_player_relics_targeter = AttachedPlayerRelicsTargeter()
attached_relic_targeter = AttachedRelicTargeter()
