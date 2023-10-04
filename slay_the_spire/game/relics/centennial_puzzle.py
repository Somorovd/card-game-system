from .reqs import Relic
from .reqs import (
    DrawCards,
    Toggle,
    EventTrigger,
    PlayerTookDamageTrigger,
    player_targeter,
)


class CentennialPuzzle(Relic):
    def __init__(self):
        super().__init__("Centennial Puzzle")
        self.add_effect(
            DrawCards(3).set_trigger(
                Toggle()
                .set_toggle_on(EventTrigger("on_combat_start"))
                .set_toggle_off(PlayerTookDamageTrigger())
                .set_trigger(PlayerTookDamageTrigger())
            )
        )
