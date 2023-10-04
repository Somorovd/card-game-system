from effect_system import EventManager
from .statable import Statable, Stat


class Player(Statable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.relics = []
        self.hand = []
        self.potions = []
        self._event_manager = EventManager()
        self.init_stats()

    def init_stats(self):
        self.add_stat("health", 100)
        self.add_stat("max_health", 100)
        self.add_stat("gold", 0)

    def equip_relic(self, relic):
        self.relics.append(relic)
        relic.on_equip()
        equip_relic_event_data = {"player": self, "relic": relic}
        res = self._event_manager.trigger_event(
            "on_player_equip_relic", equip_relic_event_data
        )

    def attack(self, target, amount):
        pre_attack_event_data = {"player": self, "amount": amount, "target": target}
        res = self._event_manager.trigger_event(
            "on_player_pre_attack", pre_attack_event_data
        )

        target.take_damage(res["amount"], self)

        post_attack_event_data = res
        res = self._event_manager.trigger_event(
            "on_player_post_attack", post_attack_event_data
        )

    def apply_healing(self, amount):
        pre_heal_event_data = {"player": self, "amount": amount}
        res = self._event_manager.trigger_event(
            "on_player_pre_heal", pre_heal_event_data
        )

        max_heal = self.get_stat("max_health") - self.get_stat("health")
        heal_amount = min(amount, max_heal)
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

    def drink_potion(self, potion):
        pre_drink_potion_event_data = {
            "player": self,
            "potion": potion,
        }
        res = self._event_manager.trigger_event(
            "on_player_pre_pre_drink_potion", pre_drink_potion_event_data
        )

        # potion does a thing

        post_drink_potion_event_data = res
        self._event_manager.trigger_event(
            "on_player_post_drink_potion", post_drink_potion_event_data
        )

    def draw_cards(self, count):
        pre_draw_event_data = {"player": self, "count": count}
        res = self._event_manager.trigger_event(
            "on_player_pre_draw_cards", pre_draw_event_data
        )

        self.hand.extend(["card"] * res["count"])

        post_draw_event_data = res
        res = self._event_manager.trigger_event(
            "on_player_post_draw_cards", post_draw_event_data
        )
