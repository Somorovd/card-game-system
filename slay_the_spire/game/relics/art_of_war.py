from .reqs import Relic
from .reqs import StatUpdate, Sequence, EventTrigger, PropertyEquals, player_targeter
from ..card import CardType


class ArtOfWar(Relic):
    def __init__(self):
        super().__init__("Art of War")
        self.add_effect(
            StatUpdate("energy", 1)
            .set_trigger(
                Sequence()
                .add_seq(EventTrigger("on_player_start_turn"))
                .add_seq(EventTrigger("on_player_end_turn"))
                .add_restart(
                    EventTrigger(
                        "on_post_play_card", PropertyEquals("type", CardType.ATTACK)
                    )
                )
            )
            .add_targeter(player_targeter)
        )
