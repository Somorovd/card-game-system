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
    def get_targets(self, event_data):
        if not self.data_type in event_data:
            return []
        prop = event_data[self.data_type]
        if isinstance(prop, list):
            return prop
        else:
            return [prop]


class AttachedPlayerTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return [effect.relic.player]


class AttachedPlayerRelicsTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return effect.relic.player.relics


class AttachedRelicTargeter(Targeter):
    def get_targets(self, effect, event_data):
        return [effect.relic]


class AttachedPlayerCounterTargeter(Targeter):
    def get_targets(self, effect, event_data):
        from .effects import Counter

        relics = effect.relic.player.relics
        counters = []
        for relic in relics:
            for effect in relic.effects:
                if isinstance(effect, Counter):
                    counters.append(effect)
        return counters


event_data_targeter = EventDataTargeter()
attached_player_targeter = AttachedPlayerTargeter()
attached_player_relics_targeter = AttachedPlayerRelicsTargeter()
attached_relic_targeter = AttachedRelicTargeter()
attached_player_counter_targeter = AttachedPlayerCounterTargeter()
