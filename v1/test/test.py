# from test import *


# def test_player_healing(players):
#     """Testing a players ability to heal"""
#     jay = players["jay"]
#     larry = players["larry"]

#     # confirm that event data is not altered
#     pre_heal_amount = 1
#     pre_heal_event_data = {"player": jay, "amount": pre_heal_amount}
#     res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
#     assert res["amount"] == pre_heal_amount

#     # confirm player health after healing
#     jay.apply_healing(2)
#     assert jay.health == 12
#     assert larry.health == 10
#     larry.apply_healing(25)
#     assert jay.health == 12
#     assert larry.health == 35
#     larry.apply_healing(100)
#     assert larry.health == 100


# def test_increase_attached_player_healing_relic(players):
#     """Testing a relic that increases the amount a player heals"""
#     heal_increase = 4
#     relic_frog_legs = Relic("Frog Legs").add_effect(
#         "on_player_pre_heal",
#         EventDataUpdate("amount", heal_increase).add_event_validator(
#             AttachedPlayerValidator()
#         ),
#     )
#     jay = players["jay"]
#     larry = players["larry"]

#     jay.add_relic(relic_frog_legs)

#     # confirm that event data is altered
#     pre_heal_amount = 1
#     pre_heal_event_data = {"player": jay, "amount": pre_heal_amount}
#     res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
#     assert res["amount"] == pre_heal_amount + heal_increase

#     # confirm resulting player health
#     health = jay.health
#     heal_amount1 = 2
#     heal_amount2 = 10
#     jay.apply_healing(heal_amount1)
#     assert jay.health == health + heal_amount1 + heal_increase
#     health = jay.health
#     jay.apply_healing(heal_amount2)
#     assert jay.health == health + heal_amount2 + heal_increase

#     # confirm no effect on other players
#     assert larry.health == 10
#     health = jay.health
#     larry.apply_healing(4)
#     assert larry.health == 14
#     assert jay.health == health


# def test_blood_leech(players):
#     get_blood_leech = lambda: (
#         Relic("Blood Leech")
#         .add_effect(
#             "on_player_pre_heal",
#             EventDataUpdate("amount", -2).add_event_validator(
#                 AttachedPlayerValidator().invert()
#             ),
#         )
#         .add_effect(
#             "on_player_post_heal",
#             Heal(2)
#             .add_targeters(attached_player_targeter)
#             .add_event_validator(AttachedPlayerValidator().invert())
#             # create a base case to prevent infinite loops
#             .add_event_validator(PropertyInRange("amount", min=1)),
#         )
#     )
#     jay = players["jay"]
#     larry = players["larry"]

#     jay.add_relic(get_blood_leech())

#     larry.apply_healing(10)
#     assert larry.health == 18
#     assert jay.health == 12

#     jay.apply_healing(4)
#     assert jay.health == 16

#     larry.add_relic(get_blood_leech())

#     jay.apply_healing(6)
#     # jay 6 -> 4 + larry 2
#     # larry 2 -> 0
#     # end
#     assert jay.health == 20
#     assert larry.health == 18


# def test_counter_tiger_claw(players):
#     counter_effect = (
#         Counter(3, EventDataUpdate("damage", 2)).add_event_validator(
#             AttachedPlayerValidator()
#         ),
#     )[0]

#     relic_tiger_claw = Relic("Tiger Claw").add_effect(
#         "on_player_pre_attack", counter_effect
#     )
#     jay = players["jay"]
#     larry = players["larry"]

#     jay.add_relic(relic_tiger_claw)

#     assert counter_effect.get_stat("count") == 0
#     jay.attack(larry, 2)
#     assert larry.health == 8
#     assert counter_effect.get_stat("count") == 1
#     jay.attack(larry, 2)
#     assert larry.health == 6
#     assert counter_effect.get_stat("count") == 2
#     jay.attack(larry, 2)
#     assert larry.health == 2
#     assert counter_effect.get_stat("count") == 0
#     jay.attack(larry, 2)
#     assert larry.health == 0
#     assert counter_effect.get_stat("count") == 1
