from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self):
        self.inverted = False

    def validate(self, relic, event_data):
        res = self._eval(relic, event_data)
        return res if not self.inverted else not res

    def invert(self):
        self.inverted = True
        return self

    @abstractmethod
    def _eval(self, relic, event_data):
        pass


class AttachedPlayerValidator(Validator):
    def _eval(self, relic, event_data):
        return event_data["player"] == relic.player


class PropertyInRange(Validator):
    def __init__(self, property, min=-float("inf"), max=float("inf")):
        super().__init__()
        self.property = property
        self.min = min
        self.max = max

    def _eval(self, relic, event_data):
        return (
            event_data[self.property] > self.min
            and event_data[self.property] < self.max
        )
