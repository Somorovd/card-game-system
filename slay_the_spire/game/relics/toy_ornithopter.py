from .reqs import Relic
from .reqs import Heal, EventTrigger, player_targeter


class ToyOrnithopter(Relic):
    def __init__(self):
        super().__init__("Toy Ornithopter")
        self.add_effect(
            Heal(5)
            .set_trigger(EventTrigger("on_player_post_drink_potion"))
            .add_targeter(player_targeter)
        )
