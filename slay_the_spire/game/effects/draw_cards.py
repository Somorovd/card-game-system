from effect_system import Effect
from ..card_manager import CardManager


class DrawCards(Effect):
    def __init__(self, count):
        super().__init__()
        self.count = count
        self._card_manager = CardManager()

    def activate(self, event_data, target):
        self._card_manager.draw_cards(self.count)
