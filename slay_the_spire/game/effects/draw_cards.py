from effect_system import Effect


class DrawCards(Effect):
    def __init__(self, count):
        super().__init__()
        self.count = count

    def activate(self, event_data, target):
        target.draw_cards(self.count)
