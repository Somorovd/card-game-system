from GameManager import GAME_MANAGER


class Player:
    def __init__(self, name):
        self.name = name
        self._health = 20
        self.attack_count = 0

    @property
    def health(self):
        return self._health

    def attack(self, target):
        target.take_damage(self.attack_count)
        self.attack_count += 1

    def apply_healing(self, amount):
        print(f"Pre Heal: {self.name} ({self.health} HP) is about to heal for {amount}")
        pre_heal_event_data = {"player": self, "amount": amount}
        res = GAME_MANAGER.trigger_event("on_player_pre_heal", pre_heal_event_data)

        print(f"Heal: {self.name} now healing for {res['amount']} HP")
        self._health += res["amount"]

        print(f"Post Heal: {self.name} has {self.health} HP\n")
        post_heal_event_data = res
        GAME_MANAGER.trigger_event("on_player_post_heal", post_heal_event_data)

    def take_damage(self, amount):
        self.health -= amount
