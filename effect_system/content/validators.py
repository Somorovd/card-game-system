from abc import ABC, abstractmethod


class Validator(ABC):
    def __init__(self):
        self.inverted = False

    def validate(self, event_data):
        res = self._eval(event_data)
        return res if not self.inverted else not res

    def invert(self):
        self.inverted = True
        return self

    @abstractmethod
    def _eval(self, event_data):
        pass


# class PropertyInRange(Validator):
#     def __init__(self, property, min=-float("inf"), max=float("inf")):
#         super().__init__()
#         self.property = property
#         self.min = min
#         self.max = max

#     def _eval(self, effect, event_data):
#         return (
#             event_data[self.property] > self.min
#             and event_data[self.property] < self.max
#         )


class PropertyEquals(Validator):
    def __init__(self, property, value):
        super().__init__()
        self.property = property
        self.value = value

    def _eval(self, event_data):
        value = self.value
        return event_data.get(self.property) == value


class OrValidator(Validator):
    def __init__(self, *validators):
        super().__init__()
        self._validators = validators

    def _eval(self, event_data):
        return any([v.validate(event_data) for v in self._validators])


class PropertyIn(Validator):
    def __init__(self, property, iter):
        super().__init__()
        self.property = property
        self.iter = iter

    def _eval(self, event_data):
        return event_data[self.property] in self.iter
