from test import *


def test_counter_targeter(players):
    jay = players["jay"]

    def get_counter():
        return Counter(2, Effect())

    counter1 = get_counter()
    counter2 = get_counter()
    counter3 = get_counter()
    effect = Effect()

    jay.add_relic(
        Relic("relic")
        .add_effect("", counter1)
        .add_effect("", counter2)
        .add_effect("", counter3)
    )
    jay.add_relic(Relic("").add_effect("", effect))

    targets = attached_player_counter_targeter.get_targets(effect, None)
    assert len(targets) == 3
    assert targets[0] == counter1
    assert targets[1] == counter2
    assert targets[2] == counter3
