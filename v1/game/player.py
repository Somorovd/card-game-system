from .game_manager import GAME_MANAGER
from .statable import Statable, Stat


class Player(Statable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stats = {
            "health": Stat("health", 10),
            "max_health": Stat("max_health", 100),
            "power": Stat("power", 2),
        }
        self.relics = []

    @property
    def health(self):
        return self.stats["health"].current

    @health.setter
    def health(self, val):
        self.stats["health"].current = min(self.stats["max_health"].current, val)

    def add_relic(self, relic):
        self.relics.append(relic)
        relic.equip_to_player(self)
        add_relic_event_data = {"player": self, "relic": relic}
        res = GAME_MANAGER.trigger_event("on_player_add_relic", add_relic_event_data)

    def attack(self, target, amount):
        pre_attack_event_data = {"player": self, "damage": amount, "target": target}
        res = GAME_MANAGER.trigger_event("on_player_pre_attack", pre_attack_event_data)

        res["target"].take_damage(self, res["damage"])

        post_attack_event_data = res
        res = GAME_MANAGER.trigger_event(
            "on_player_post_attack", post_attack_event_data
        )

    def apply_healing(self, amount):
        pre_heal_event_data = {"player": self, "amount": amount}
        res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)
        self.health += res["amount"]

        post_heal_event_data = res
        GAME_MANAGER.trigger_event("on_player_post_heal", post_heal_event_data)

    def take_damage(self, source, amount):
        pre_take_damage_event_data = {
            "player": self,
            "damage": amount,
            "source": source,
        }
        res = GAME_MANAGER.trigger_event(
            "on_player_pre_take_damage", pre_take_damage_event_data
        )

        self.health -= res["damage"]

        # if the post_take_damage event happens here, now, it will happen before the
        # attacker's post_attack event

        post_take_damage_event_data = res
        GAME_MANAGER.trigger_event(
            "on_player_post_take_damage", post_take_damage_event_data
        )
