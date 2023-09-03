from GameManager import GAME_MANAGER
from statblocks import PlayerStatBlock


class Player:
    def __init__(self, name):
        self.name = name
        self.stats = PlayerStatBlock()
        self.modifiers = PlayerStatBlock(is_modifier=True)
        self.relics = []

    @property
    def health(self):
        return self.stats.health + self.modifiers.health

    def add_relic(self, relic):
        print(f"{self.name} is equipping {relic.name}")
        self.relics.append(relic)
        relic.equip_to_player(self)
        print()
        add_relic_event_data = {"player": self, "relic": relic}
        GAME_MANAGER.trigger_event("on_player_add_relic", add_relic_event_data)

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
        self.stats.health += res["amount"]

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
        self.stats.health -= res["damage"]

        # if the post_take_damage event happens here, now, it will happen before the
        # attacker's post_attack event

        print(f"Post Take Damage: {self.name} has {self.health} HP")
        post_take_damage_event_data = res
        GAME_MANAGER.trigger_event(
            "on_player_post_take_damage", post_take_damage_event_data
        )
