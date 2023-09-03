from EventManager import Listener


class Effect(Listener):
    def __init__(self):
        self.relic = None

    def on_add(self, relic):
        self.relic = relic

    def on_equip(self, player):
        pass

    def on_unequip(self, player):
        pass

    def validate(self, event_data):
        return not self.relic.player == None

    def activate(self, event_data):
        pass


class IncreaseHealing(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def validate(self, event_data):
        return (
            super().validate(event_data) and event_data["player"] == self.relic.player
        )

    def activate(self, event_data):
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

    def activate(self, event_data):
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

    def activate(self, event_data):
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

    def activate(self, event_data):
        self.relic.data["counter"] += 1
        print(
            f"{self.relic.name} increases count by 1. Now at {self.relic.data['counter']}/{self.count}"
        )

        if self.relic.data["counter"] >= self.count:
            prev = event_data[self.property]
            event_data[self.property] += self.amount
            self.relic.data["counter"] = 0
            current = event_data[self.property]
            print(
                f"ACTIVATE: {self.relic.name} increases {self.property} from {prev} to {current}."
            )


class ChangeRelicTiming(Effect):
    # could have a different one to set to a specific value
    # may need to specify type of counter / counting property
    def __init__(self, amount):
        super().__init__()
        self.amount = amount
        self.affected_effects = []

    def modify_relic_effect(self, relic, effect):
        if not type(effect) == CounterChangeAmount:
            return

        prev = effect.count
        effect.count = max(0, effect.count + self.amount)
        curr = effect.count
        print(
            f"Updating {effect.property} counter on {relic.name} from {prev} to {curr}"
        )
        self.affected_effects.append(effect)

    def on_equip(self, player):
        for relic in player.relics:
            for effect in relic.effects:
                self.modify_relic_effect(relic, effect)

    def on_unequip(self, player):
        for effect in self.affected_effects:
            effect.count = max(0, effect - self.amount)
        self.affected_effects = []

    def validate(self, event_data):
        return (
            super().validate(event_data) and event_data["player"] == self.relic.player
        )

    def activate(self, event_data):
        # event is an on_player_add_relic
        relic = event_data.get("relic")
        if not relic:
            return

        for effect in relic.effects:
            self.modify_relic_effect(relic, effect)
