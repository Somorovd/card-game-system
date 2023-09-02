from abc import ABC, abstractmethod


class Effect(ABC):
    def __init__(self):
        self.relic = None

    def on_add(self, relic):
        self.relic = relic

    def validate(self, event_data):
        return self.relic.player != None

    @abstractmethod
    def listener(self, event_data):
        pass


class IncreaseHealing(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def validate(self, event_data):
        return (
            super().validate(event_data) and event_data["player"] == self.relic.player
        )

    def listener(self, event_data):
        if not self.validate(event_data):
            return

        print(
            f"{self.relic.name} increasing healing from {event_data['amount']} to {event_data['amount'] + self.amount}"
        )
        event_data["amount"] += self.amount


class LeechReduce(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def validate(self, event_data):
        return (
            super().validate(event_data)
            and not event_data["player"] == self.relic.player
        )

    def listener(self, event_data):
        if not self.validate(event_data):
            return

        print(
            f"{self.relic.name} reducing {event_data['player'].name} healing by {self.amount}"
        )
        event_data["amount"] -= self.amount


class LeechHeal(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def validate(self, event_data):
        return (
            super().validate(event_data)
            and not event_data["player"] == self.relic.player
        )

    def listener(self, event_data):
        if not self.validate(event_data):
            return

        print(
            f"{self.relic.name} is healing {self.relic.player.name} for {self.amount}"
        )
        self.relic.player.apply_healing(self.amount)


class CounterChangeAmount(Effect):
    def __init__(self, property, amount, count):
        super().__init__()
        self.property = property
        self.amount = amount
        self.count = count

    def on_add(self, relic):
        super().on_add(relic)
        relic.data["counter"] = 0

    def validate(self, event_data):
        return (
            super().validate(event_data) and event_data["player"] == self.relic.player
        )

    def listener(self, event_data):
        if not self.validate(event_data):
            return

        self.relic.data["counter"] += 1
        print(
            f"{self.relic.name} increases count by 1. Now at {self.relic.data['counter']}/{self.count}"
        )

        if self.relic.data["counter"] == self.count:
            prev = event_data[self.property]
            event_data[self.property] += self.amount
            self.relic.data["counter"] = 0
            current = event_data[self.property]
            print(
                f"ACTIVATE: {self.relic.name} increases {self.property} from {prev} to {current}."
            )
