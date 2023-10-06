from .reqs import Relic
from .reqs import EventDataUpdate, Sequence, EventTrigger, AddOp


class BagOfPreparation(Relic):
    def __init__(self):
        super().__init__("Bag of Preparation")
        self.add_effect(
            EventDataUpdate("count", AddOp(2)).set_trigger(
                Sequence()
                .add_seq(EventTrigger("on_combat_start"))
                .add_seq(EventTrigger("on_pre_draw_cards"))
                .add_restart(EventTrigger("on_player_turn_end"))
            )
        )
