from effect_system import Effect


class EventDataUpdate(Effect):
    def __init__(self, data_type, amount):
        super().__init__()
        self.data_type = data_type
        self.amount = amount

    def activate(self, event_data, target):
        if self.data_type in event_data:
            event_data[self.data_type] += self.amount
