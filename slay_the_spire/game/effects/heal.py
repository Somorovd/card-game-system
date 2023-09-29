from effect_system import Effect


class Heal(Effect):
    def __init__(self, amount):
        super().__init__()
        self.amount = amount

    def activate(self, event_data, target):
        target.apply_healing(self.amount)
