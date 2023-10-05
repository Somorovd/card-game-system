from .reqs import Relic
from .reqs import StatUpdate, EventTrigger, player_targeter


class CeramicFish(Relic):
    def __init__(self):
        super().__init__("Ceramic Fish")
        self.add_effect(
            StatUpdate("gold", 9)
            .set_trigger(EventTrigger("on_post_add_card"))
            .add_targeter(player_targeter)
        )
