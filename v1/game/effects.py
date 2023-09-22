from .game_manager import GAME_MANAGER, Subject
from .statable import Statable, Stat
from .targeters import *


class Effect:
    def __init__(self, game_manager=GAME_MANAGER):
        # self.relic = None
        self._event_validators = {}
        self._targeters = []
        self._is_listening = False
        self.game_manager = game_manager

    def set_event_validator(self, event_name, *validators):
        self._event_validators[event_name] = validators
        return self

    def add_targeter(self, targeter):
        self._targeters.append(targeter)
        return self

    def get_targets(self, event_data):
        targets = []
        for targeter in self._targeters:
            targets.extend(targeter.get_targets(event_data))
        return targets

    def set_listening(self, should_listen):
        if self._is_listening == should_listen:
            return
        self._is_listening = should_listen
        for event_name in self._event_validators:
            if self._is_listening:
                self.game_manager.add_listener(event_name, self.update)
            else:
                self.game_manager.remove_listener(event_name, self.update)

    def update(self, event_name, event_data):
        if self.validate_event(event_name, event_data):
            if self._targeters:
                self.activate_on_targets(event_data)
            else:
                self.activate(event_data)

    def validate_event(self, event_name, event_data):
        validators = self._event_validators.get(event_name)
        if not validators:
            return True
        return all([v.validate(event_data) for v in validators])

    def activate_on_targets(self, event_data):
        for target in self.get_targets(event_data):
            self.activate(event_data, target)

    def activate(self, event_data, target):
        pass

    # def on_add_to_relic(self, relic, event_name):
    #     self.relic = relic
    #     self.event_name = event_name

    # def on_equip(self, player):
    #     pass

    # def on_unequip(self, player):
    #     pass


# class EffectDecorator(Effect):
#     def __init__(self, effect):
#         super().__init__()
#         self.effect = effect

#     def on_add_to_relic(self, relic, event_name):
#         super().on_add_to_relic(relic, event_name)
#         self.effect.on_add_to_relic(relic, event_name)

#     def on_equip(self, player):
#         super().on_equip(player)
#         self.effect.on_equip(player)


# class EffectSubject(Subject, Effect):
#     def __init__(self):
#         super().__init__()
#         self.relic = None
#         self.validators = []
#         self.targeters = []


# class EventDataUpdate(Effect):
#     def __init__(self, data_type, amount):
#         super().__init__()
#         self.data_type = data_type
#         self.amount = amount
#         self.add_targeters(event_data_targeter)

#     def _apply(self, event_data, target):
#         print(
#             f"{self.relic.name} increasing {self.data_type} from {target[self.data_type]} to {target[self.data_type] + self.amount}"
#         )
#         target[self.data_type] += self.amount


"""
# class StatUpdate(Effect):
#     def __init__(self, stat_type, amount):
#         super().__init__()
#         self.stat_type = stat_type
#         self.amount = amount

#     def activate(self, event_data):
#         print(
#             f"{self.relic.name} is updating {self.stat_type} on {self.relic.player.name} from {self.amount} to {self.relic.player.stats[self.stat_type] + self.amount}"
#         )
#         self.relic.player.updateStat(self.stat_type, self.amount)
"""


# class Heal(Effect):
#     def __init__(self, amount):
#         super().__init__()
#         self.amount = amount

#     def _apply(self, event_data, target):
#         print(f"{self.relic.name} is healing {target.name} for {self.amount}")
#         target.apply_healing(self.amount)


# class Counter(EffectDecorator, Statable):
#     def __init__(self, max_count, effect):
#         super().__init__(effect)
#         self.stats = {
#             "max_count": Stat("max_count", max_count),
#             "count": Stat("count", 0),
#         }

#     def activate(self, event_data):
#         self.adjust_stat("count", 1)

#         if self.get_stat("count") >= self.get_stat("max_count"):
#             self.effect.activate(event_data)
#             self.adjust_stat("count", -self.get_stat("count"))


# class NTimes(EffectDecorator):
#     def __init__(self, max_count, effect):
#         super().__init__(effect)
#         self.max_count = max_count
#         self.curr_count = 0

#     def activate(self, event_data):
#         self.curr_count += 1
#         self.effect.activate(event_data)
#         if self.curr_count >= self.max_count:
#             GAME_MANAGER.remove_listener(self.event_name, self.update)


# class StatModifierEffect(EffectSubject):
#     def __init__(self, stat_type, amount):
#         super().__init__()
#         self.stat_type = stat_type
#         self.amount = amount

#     def on_add_to_relic(self, relic, event_name):
#         super().on_add_to_relic(relic, event_name)
#         self.relic.add_stat_source(self.stat_type, self)

#     def on_equip(self, player):
#         for targerter in self.targeters:
#             for target in targerter.get_targets(self, None):
#                 target.add_stat_source(self.stat_type, self.relic)

#     def activate(self, event_data):
#         stat_update_event_data = {"stat": self.stat_type, "amount": self.amount}
#         self.trigger_event("on_stat_update", stat_update_event_data)


# class ChangeRelicTiming(Effect):
#     # could have a different one to set to a specific value
#     # may need to specify type of counter / counting property
#     def __init__(self, amount):
#         super().__init__()
#         self.amount = amount
#         self.affected_effects = []

#     def modify_relic_effect(self, relic, effect):
#         if not type(effect) == Counter:
#             return

#         prev = effect.max_count
#         effect.max_count = max(0, effect.max_count + self.amount)
#         curr = effect.max_count
#         print(
#             f"Updating {effect.property} counter on {relic.name} from {prev} to {curr}"
#         )
#         self.affected_effects.append(effect)

#     def on_equip(self, player):
#         for relic in player.relics:
#             for effect in relic.effects:
#                 self.modify_relic_effect(relic, effect)

#     def on_unequip(self, player):
#         for effect in self.affected_effects:
#             effect.count = max(0, effect.max_count - self.amount)
#         self.affected_effects = []

#     def activate(self, event_data):
#         # event is an on_player_add_relic
#         relic = event_data.get("relic")
#         if not relic:
#             return

#         for effect in relic.effects:
#             self.modify_relic_effect(relic, effect)
