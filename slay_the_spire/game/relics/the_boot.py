from .reqs import Relic
from .reqs import EventDataUpdate, EventTrigger, MaxOp


class TheBoot(Relic):
    def __init__(self):
        super().__init__("The Boot")
        self.add_effect(
            EventDataUpdate("amount", MaxOp(5)).set_trigger(
                EventTrigger("on_enemy_pre_take_damage")
            )
        )
