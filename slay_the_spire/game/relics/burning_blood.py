from .reqs import *


class BurningBlood(Relic):
    def __init__(self):
        super().__init__("Burning Blood")
        self.add_effect(
            Heal(6)
            .set_trigger(EventTrigger("on_combat_end"))
            .add_targeter(player_targeter)
        )
