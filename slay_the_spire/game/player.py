from effect_system import EventManager
from .statable import Statable, Stat


class Player(Statable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self._event_manager = EventManager()
#         self.relics = []
        self.init_stats()

#     def add_relic(self, relic):
#         self.relics.append(relic)
#         relic.equip_to_player(self)
#         add_relic_event_data = {"player": self, "relic": relic}
#         res = EVENT_MANAGER.trigger_event("on_player_add_relic", add_relic_event_data)

    def init_stats(self):
        self.add_stat("health", 100)
        self.add_stat("max_health", 100)

    def attack(self, target, amount):
        pre_attack_event_data = {"player": self, "amount": amount, "target": target}
        res = self._event_manager.trigger_event("on_player_pre_attack", pre_attack_event_data)

        target.take_damage(amount, self)

        post_attack_event_data = res
        res = self._event_manager.trigger_event(
            "on_player_post_attack", post_attack_event_data
        )

    def apply_healing(self, amount):
        pre_heal_event_data = {"player": self, "amount": amount}
        res = self._event_manager.trigger_event("on_player_pre_heal", pre_heal_event_data)

        max_heal = self.get_stat("max_health") - self.get_stat("health")
        heal_amount = min(amount, max_heal);
        self.stats["health"].adjust_current(heal_amount)

        post_heal_event_data = res
        post_heal_event_data["heal"] = heal_amount
        self._event_manager.trigger_event("on_player_post_heal", post_heal_event_data)

    def take_damage(self, amount, source):
        pre_take_damage_event_data = {
            "player": self,
            "amount": amount,
            "source": source,
        }
        res = self._event_manager.trigger_event(
            "on_player_pre_take_damage", pre_take_damage_event_data
        )

        self.stats["health"].adjust_current(-amount)

        post_take_damage_event_data = res
        self._event_manager.trigger_event(
            "on_player_post_take_damage", post_take_damage_event_data
        )
