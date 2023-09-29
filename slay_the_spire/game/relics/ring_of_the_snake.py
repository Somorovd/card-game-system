from .reqs import *


class RingOfTheSnake(Relic):
    def __init__(self):
        super().__init__("Ring of the Snake")
        self.add_effect(
            EventDataUpdate("count", 2).set_trigger(
                Toggle()
                .set_toggle_on(EventTrigger("on_combat_start"))
                .set_toggle_off(EventTrigger("on_player_post_draw_cards"))
                .set_trigger(EventTrigger("on_player_pre_draw_cards"))
            )
        )
