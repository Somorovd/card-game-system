from Player import Player
from relics import *
from effects import *


relic_frog_legs = Relic("Frog Legs").add_effect(
    "on_player_pre_heal", IncreaseHealing(4)
)

relic_blood_leech = (
    Relic("Blood Leech")
    .add_effect("on_player_pre_heal", LeechReduce(2))
    .add_effect("on_player_post_heal", LeechHeal(2))
)

relic_tiger_claw = Relic("Tiger Claw").add_effect(
    "on_player_pre_attack", CounterChangeAmount("damage", 5, 3)
)

jay = Player("Jay")
larry = Player("Larry")
relic_frog_legs.attach_to(jay)
relic_tiger_claw.attach_to(jay)
relic_blood_leech.attach_to(larry)

jay.apply_healing(10)
larry.apply_healing(5)

jay.attack(larry, 2)
jay.attack(larry, 2)
jay.attack(larry, 2)
jay.attack(larry, 2)
