from GameManager import GAME_MANAGER


class Relic:
    def __init__(self, name):
        self.name = name
        self.player = None
        self.data = {}

    def attach_to(self, player):
        self.player = player

    def add_listener(self, event_name, listener):
        GAME_MANAGER.add_listener(event_name, listener, relic=self)
        return self


def increase_healing(x):
    def listener(event_data, relic):
        if not relic.player or not event_data["player"] == relic.player:
            return

        print(
            f"{relic.name} increasing healing from {event_data['amount']} to {event_data['amount'] + x}"
        )
        event_data["amount"] += x

    return listener


def leech_reduce(x):
    def listener(event_data, relic):
        if not relic.player or event_data["player"] == relic.player:
            return

        print(f"{relic.name} reducing {event_data['player'].name} healing by {x}")
        event_data["amount"] -= x

    return listener


def leech_heal(x):
    def listener(event_data, relic):
        if not relic.player or event_data["player"] == relic.player:
            return
        print(f"{relic.name} is healing {relic.player.name} for {x}")
        relic.player.apply_healing(x)

    return listener


def counter_change_amount(field, t, amount):
    def listener(event_data, relic):
        if not relic.player or not event_data["player"] == relic.player:
            return

        if not relic.data.get("count"):
            relic.data["count"] = 0

        relic.data["count"] += 1
        print(f"{relic.name} increases count by 1. Now at {relic.data['count']}/{t}")

        if relic.data["count"] == t:
            event_data[field] += amount
            relic.data["count"] = 0
            print(
                f"ACTIVATE: {relic.name} increases {field} from {event_data[field] - amount} to {event_data[field]}."
            )

    return listener
