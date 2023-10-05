from .reqs import Relic
from .reqs import StatUpdate, Repeat, EventTrigger, PropertyEquals, player_targeter
from ..card import CardType


class Nunchaku(Relic):
    def __init__(self):
        super().__init__("Nunchaku")
        self.add_effect(
            StatUpdate("energy", 1)
            .set_trigger(
                Repeat(
                    10,
                    EventTrigger(
                        "on_post_play_card", PropertyEquals("type", CardType.ATTACK)
                    ),
                )
            )
            .add_targeter(player_targeter)
        )
