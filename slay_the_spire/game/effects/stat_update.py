from effect_system import Effect


class StatUpdate(Effect):
    def __init__(self, stat_type, amount):
        super().__init__()
        self.stat_type = stat_type
        self.amount = amount

    def activate(self, event_data, target):
        target.stats[self.stat_type].adjust_current(self.amount)
