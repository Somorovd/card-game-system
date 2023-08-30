from GameManager import GAME_MANAGER


class Player:
    def __init__(self, name):
        self.name = name
        self._health = 20

        # GAME_MANAGER.add_listener("on_player_pre_attack", self._pre_damage_listener)
        # GAME_MANAGER.add_listener("on_player_post_attack", self._post_damage_listener)

    @property
    def health(self):
        return self._health

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
        res = GAME_MANAGER.trigger_event("on_player_post_attack", res)

    def apply_healing(self, amount):
        print(f"Pre Heal: {self.name} ({self.health} HP) is about to heal for {amount}")
        pre_heal_event_data = {"player": self, "amount": amount}
        res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)

        print(f"Heal: {self.name} now healing for {res['amount']} HP")
        self._health += res["amount"]

        print(f"Post Heal: {self.name} has {self.health} HP\n")
        post_heal_event_data = res
        GAME_MANAGER.trigger_event("on_player_post_heal", post_heal_event_data)

    # def _pre_damage_listener(event_data):
    #     if event_data["target"] == self:
    #         GAME_MANAGER.trigger_event("on_player_pre_take_damage", event_data)

    # def _post_damage_listener(event_data):
    #     if event_data["target"] == self:
    #         GAME_MANAGER.trigger_event("on_player_post_take_damage", event_data)

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
        self._health -= res["damage"]

        # if the post_take_damage event happens here, now, it will happen before the
        # attacker's post_attack event

        print(f"Post Take Damage: {self.name} has {self.health} HP")
        post_take_damage_event_data = res
        GAME_MANAGER.trigger_event(
            "on_player_post_take_damage", post_take_damage_event_data
        )
