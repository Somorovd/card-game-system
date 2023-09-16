from .game_manager import GAME_MANAGER
from .statable import Statable, Stat


class Player(Statable):
    def __init__(self, name):
        super().__init__()
        self.name = name
        self.stats = {
            "health": Stat(10),
            "max_health": Stat(100),
            "power": Stat(2),
        }
        self.relics = []

    @property
    def health(self):
        return self.stats["health"].current

    @health.setter
    def health(self, val):
        self.stats["health"].current = min(self.stats["max_health"].current, val)

    def add_relic(self, relic):
        print(f"{self.name} is equipping {relic.name}")
        self.relics.append(relic)
        relic.equip_to_player(self)
        print()
        add_relic_event_data = {"player": self, "relic": relic}
        res = GAME_MANAGER.trigger_event("on_player_add_relic", add_relic_event_data)

    def attack(self, target, amount):
        print(f"Pre Attack: {self.name} is about to attack {target.name} for {amount}")
        pre_attack_event_data = {"player": self, "damage": amount, "target": target}
        res = GAME_MANAGER.trigger_event("on_player_pre_attack", pre_attack_event_data)

        print(
            f"Attack: {self.name} is attacks {res['target'].name} ({res['target'].health} HP) for {res['damage']}"
        )
        res["target"].take_damage(self, res["damage"])

        print(f"Post Attack: {res['target'].name} has {res['target'].health}\n")
        post_attack_event_data = res
        res = GAME_MANAGER.trigger_event(
            "on_player_post_attack", post_attack_event_data
        )

    def apply_healing(self, amount):
        print(f"Pre Heal: {self.name} ({self.health} HP) is about to heal for {amount}")
        pre_heal_event_data = {"player": self, "amount": amount}
        res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)

        print(f"Heal: {self.name} now healing for {res['amount']} HP")
        self.health += res["amount"]

        print(f"Post Heal: {self.name} has {self.health} HP\n")
        post_heal_event_data = res
        GAME_MANAGER.trigger_event("on_player_post_heal", post_heal_event_data)

    def take_damage(self, source, amount):
        print(f"Pre Take Damage: {self.name} is about to take {amount} damage")
        pre_take_damage_event_data = {
            "player": self,
            "damage": amount,
            "source": source,
        }
        res = GAME_MANAGER.trigger_event(
            "on_player_pre_take_damage", pre_take_damage_event_data
        )

        print(f"Take Damage: {self.name} takes {res['damage']} damage")
        self.health -= res["damage"]

        # if the post_take_damage event happens here, now, it will happen before the
        # attacker's post_attack event

        print(f"Post Take Damage: {self.name} has {self.health} HP")
        post_take_damage_event_data = res
        GAME_MANAGER.trigger_event(
            "on_player_post_take_damage", post_take_damage_event_data
        )
