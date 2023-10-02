from .reqs import Relic
from .reqs import EventDataUpdate, Toggle, EventTrigger


class Akabako(Relic):
    def __init__(self):
        super().__init__("Akabako")
        self.add_effect(
            EventDataUpdate("amount", 8).set_trigger(
                Toggle()
                .set_toggle_on(EventTrigger("on_combat_start"))
                .set_toggle_off(EventTrigger("on_player_post_attack"))
                .set_trigger(EventTrigger("on_player_pre_attack"))
            )
        )
