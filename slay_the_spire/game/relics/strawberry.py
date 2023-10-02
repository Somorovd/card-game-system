from .reqs import Relic
from .reqs import StatUpdate, OnEquipTrigger, player_targeter


class Strawberry(Relic):
    def __init__(self):
        super().__init__("Strawberry")
        self.add_effect(
            StatUpdate("max_health", 7)
            .set_trigger(OnEquipTrigger())
            .add_targeter(player_targeter)
        )
