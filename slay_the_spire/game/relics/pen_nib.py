from .reqs import Relic
from .reqs import Repeat, EventTrigger, EventDataUpdate, MultOp


class PenNib(Relic):
    def __init__(self):
        super().__init__("Pen Nib")
        self.add_effect(
            EventDataUpdate("amount", MultOp(2)).set_trigger(
                Repeat(10, EventTrigger("on_player_pre_attack"))
            )
        )
