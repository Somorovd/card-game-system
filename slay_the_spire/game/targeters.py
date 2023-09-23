
# class AttachedPlayerTargeter(Targeter):
#     def get_targets(self, effect, event_data):
#         return [effect.relic.player]


# class AttachedPlayerRelicsTargeter(Targeter):
#     def get_targets(self, effect, event_data):
#         return effect.relic.player.relics


# class AttachedRelicTargeter(Targeter):
#     def get_targets(self, effect, event_data):
#         return [effect.relic]


# class AttachedPlayerCounterTargeter(Targeter):
#     def get_targets(self, effect, event_data):
#         from .effects import Counter

#         relics = effect.relic.player.relics
#         counters = []
#         for relic in relics:
#             for effect in relic.effects:
#                 if isinstance(effect, Counter):
#                     counters.append(effect)
#         return counters



# attached_player_targeter = AttachedPlayerTargeter()
# attached_player_relics_targeter = AttachedPlayerRelicsTargeter()
# attached_relic_targeter = AttachedRelicTargeter()
# attached_player_counter_targeter = AttachedPlayerCounterTargeter()
