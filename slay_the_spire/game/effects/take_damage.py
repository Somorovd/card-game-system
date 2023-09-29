from effect_system import Effect


class TakeDamage(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def activate(self, event_data, target):
        target.take_damage(self.amount, self)
