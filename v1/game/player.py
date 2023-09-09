from .game_manager import GAME_MANAGER, Subject
from .statblocks import PlayerStatBlock


class Player:
    def __init__(self, name):
        self.name = name
        self.stats = {
            "health": {"base": 10, "current": 10, "mod": 0, "sources": {}},
            "max_health": {"base": 10, "current": 10, "mod": 0, "sources": {}},
            "power": {"base": 2, "current": 2, "mod": 0, "sources": {}},
        }
        self.relics = []

    @property
    def health(self):
        return self.stats["health"]["current"]

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
        self.stats["health"]["current"] += res["amount"]
        self.stats["health"]["current"] = max(
            self.stats["health"]["current"], self.stats["max_health"]["current"]
        )

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
        self.stats["health"]["current"] -= res["damage"]

        # if the post_take_damage event happens here, now, it will happen before the
        # attacker's post_attack event

        print(f"Post Take Damage: {self.name} has {self.health} HP")
        post_take_damage_event_data = res
        GAME_MANAGER.trigger_event(
            "on_player_post_take_damage", post_take_damage_event_data
        )

    def add_stat_modifier(self, stat, source):
        if not stat in self.stats:
            raise TypeError(f"Player has no stat '{stat}'")
        if not issubclass(type(source), Subject):
            raise TypeError("Modifier source must implament Subject interface")

        s = self.stats[stat]
        s["sources"][source] = 0
        print(f"{self.name} now listening to {source.name} for {stat} updates")

        def _update_func(event_data):
            if event_data["stat"] != stat:
                return

            amount = event_data["amount"]
            current = s["sources"][source]
            diff = amount - current
            print(
                f"{self.name} had {stat}: {s['current']}, now has {stat}: {s['current'] + diff}"
            )
            s["mod"] += diff
            s["current"] += diff
            s["sources"][source] = amount

        source.add_listener("on_mod_update", _update_func)
