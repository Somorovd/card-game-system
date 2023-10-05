from .reqs import Relic
from .reqs import StatUpdate, Repeat, EventTrigger, player_targeter


class HappyFlower(Relic):
    def __init__(self):
        super().__init__("Happy Flower")
        self.add_effect(
            StatUpdate("energy", 1)
            .set_trigger(Repeat(3, EventTrigger("on_player_start_turn")))
            .add_targeter(player_targeter)
        )
