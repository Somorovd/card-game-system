from .reqs import *


class MawBank(Relic):
    def __init__(self):
        super().__init__("Maw Bank")
        self.add_effect(
            StatUpdate("gold", 12)
            .set_trigger(
                Toggle()
                .set_init_toggled(True)
                .set_toggle_off(EventTrigger("on_player_shop_purchase"))
                .set_trigger(EventTrigger("on_player_climb_floor"))
            )
            .add_targeter(player_targeter)
        )
