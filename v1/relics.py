from GameManager import GAME_MANAGER


class Relic:
    def __init__(self, name):
        self.name = name
        self.player = None

    def attach_to(self, player):
        self.player = player

    def add_listener(self, event_name, listener):
        GAME_MANAGER.add_listener(event_name, listener, self)
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
