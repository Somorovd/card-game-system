from .reqs import *


class BronzeScales(Relic):
    def __init__(self):
        super().__init__("Bronze Scales")
        self.add_effect(
            TakeDamage(3)
            .set_trigger(
                EventTrigger(
                    "on_player_post_take_damage",
                    PropertyOneOf("source", GameManager().enemies),
                )
            )
            .add_targeter(EventDataPropertyTargeter("source"))
        )
