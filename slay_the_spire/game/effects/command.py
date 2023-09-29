from effect_system import Effect


class CommandEffect(Effect):
    def __init__(self, command):
        super().__init__()
        self.command = command

    def activate(self, event_data, target):
        self.command.invoke(event_data, target)
