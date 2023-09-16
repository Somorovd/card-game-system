from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self, invert=False):
        self.invert = invert

    def validate(self, relic, event_data):
        res = self._eval(relic, event_data)
        return res if not self.invert else not res

    @abstractmethod
    def _eval(relic, event_data):
        pass


class AttachedPlayerValidator(Validator):
    def _eval(self, relic, event_data):
        return event_data["player"] == relic.player
