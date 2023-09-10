from game import *

jay = Player("Jay")
larry = Player("Larry")
# jay.add_relic(relic_frog_legs)
# jay.add_relic(relic_tiger_claw)
larry.add_relic(relic_lion_heart)
mod = StatModifier("max_health", 3)
relic_lion_heart.add_stat_modifier("max_health", mod)
mod.activate(None)
# larry.add_relic(relic_blood_leech)

# jay.apply_healing(10)
# larry.apply_healing(5)

# jay.attack(larry, 2)
# jay.attack(larry, 2)
# jay.attack(larry, 2)
# jay.attack(larry, 2)

# jay.add_relic(relic_hawk_eye)
# jay.attack(larry, 2)
