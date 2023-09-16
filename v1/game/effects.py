from .game_manager import GAME_MANAGER, Subject


class Effect:
    def __init__(self):
        self.relic = None
        self.validators = []

    def add_validator(self, validator):
        self.validators.append(validator)
        return self

    def validate(self, event_data):
        return all([v.validate(self.relic, event_data) for v in self.validators])

    def on_add_to_relic(self, relic, event_name):
        self.relic = relic
        self.event_name = event_name

    def on_equip(self, player):
        pass

    def on_unequip(self, player):
        pass

    def update(self, event_data):
        if self.validate(event_data):
            self.activate(event_data)

    def activate(self, event_data):
        pass


class IncreaseHealing(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def activate(self, event_data):
        print(
            f"{self.relic.name} increasing healing from {event_data['amount']} to {event_data['amount'] + self.amount}"
        )
        event_data["amount"] += self.amount


class LeechReduce(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def activate(self, event_data):
        print(
            f"{self.relic.name} reducing {event_data['player'].name} healing by {self.amount}"
        )
        event_data["amount"] -= self.amount


class LeechHeal(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

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
        self.max_count = count
        self.curr_count = 0

    def activate(self, event_data):
        self.curr_count += 1
        print(
            f"{self.relic.name} increases count by 1. Now at {self.curr_count}/{self.max_count}"
        )

        if self.curr_count >= self.max_count:
            prev = event_data[self.property]
            event_data[self.property] += self.amount
            self.curr_count = 0
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

        prev = effect.max_count
        effect.max_count = max(0, effect.max_count + self.amount)
        curr = effect.max_count
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
            effect.count = max(0, effect.max_count - self.amount)
        self.affected_effects = []

    def activate(self, event_data):
        # event is an on_player_add_relic
        relic = event_data.get("relic")
        if not relic:
            return

        for effect in relic.effects:
            self.modify_relic_effect(relic, effect)


class NTimes(Effect):
    def __init__(self, count, effect):
        super().__init__()
        self.effect = effect
        self.max_count = count
        self.curr_count = 0

    def on_add_to_relic(self, relic, event_name):
        super().on_add_to_relic(relic, event_name)
        self.effect.on_add_to_relic(relic, event_name)

    def on_equip(self, player):
        super().on_equip(player)
        self.effect.on_equip(player)

    def activate(self, event_data):
        self.curr_count += 1
        self.effect.activate(event_data)
        if self.curr_count >= self.max_count:
            GAME_MANAGER.remove_listener(self.event_name, self.update)


class StatModifier(Subject, Effect):
    def __init__(self, stat_type, amount):
        super().__init__()
        self.stat_type = stat_type
        self.amount = amount

    def on_equip(self, player):
        self.relic.add_stat_source(self.stat_type, self)
        player.add_stat_source(self.stat_type, self.relic)

    def activate(self, _event_data):
        # print(
        #     f"{self.relic.name} is modifying {self.stat_type} by {self.amount} on {self.relic.player.name}"
        # )
        stat_update_event_data = {"stat": self.stat_type, "amount": self.amount}
        self.trigger_event("on_stat_update", stat_update_event_data)
