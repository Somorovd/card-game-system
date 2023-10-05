from .reqs import Relic
from .reqs import Toggle, Repeat, EventDataUpdate, SetOp, EventTrigger, PropertyEquals
from ..card import CardType


class Omamori(Relic):
    def __init__(self):
        super().__init__("Omamori")
        AddCurseTrigger = lambda: EventTrigger(
            "on_pre_add_card", PropertyEquals("type", CardType.CURSE)
        )
        self.add_effect(
            EventDataUpdate("card", SetOp(None)).set_trigger(
                Toggle()
                .set_trigger(AddCurseTrigger())
                .set_toggle_off(Repeat(2, AddCurseTrigger()))
                .set_init_toggled(True)
            )
        )
