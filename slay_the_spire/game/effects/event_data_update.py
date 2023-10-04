from effect_system import Effect


class EventDataUpdate(Effect):
    def __init__(self, data_type, op):
        super().__init__()
        self.data_type = data_type
        self.op = op

    def activate(self, event_data, target):
        if self.data_type in event_data:
            event_data[self.data_type] = self.op.eval(event_data[self.data_type])
