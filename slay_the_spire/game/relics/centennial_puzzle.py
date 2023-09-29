from .reqs import *


class CentennialPuzzle(Relic):
    def __init__(self):
        super().__init__("Centennial Puzzle")
        self.add_effect(
            DrawCards(3)
            .set_trigger(
                Toggle()
                .set_toggle_on(EventTrigger("on_combat_start"))
                .set_toggle_off(
                    EventTrigger(
                        "on_player_post_take_damage", PropertyInRange("amount", min=1)
                    )
                )
                .set_trigger(
                    EventTrigger(
                        "on_player_post_take_damage", PropertyInRange("amount", min=1)
                    )
                )
            )
            .add_targeter(player_targeter)
        )
