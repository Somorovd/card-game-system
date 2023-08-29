from Player import Player
from relics import *


relic_frog_legs = Relic("Frog Legs").add_listener(
    "on_player_pre_heal", increase_healing(4)
)

relic_blood_leech = (
    Relic("Blood Leech")
    .add_listener("on_player_pre_heal", leech_reduce(2))
    .add_listener("on_player_post_heal", leech_heal(2))
)

jay = Player("Jay")
larry = Player("Larry")
relic_frog_legs.attach_to(jay)
relic_blood_leech.attach_to(larry)

jay.apply_healing(10)
larry.apply_healing(5)
