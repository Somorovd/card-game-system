from effect_system.content.event_manager import EventManager


class CardManager:
    _instance = None

    def __new__(cls):
        if cls._instance:
            return cls._instance
        else:
            cls._instance = super(CardManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True
        self._event_manager = EventManager()
        self.hand = []
        self.deck = []
        self.discard = []
        self.exhaust = []

    def reset(self):
        self._initialized = False
        self.__init__()

    def draw_cards(self, count):
        pre_draw_event_data = {"count": count}
        res = self._event_manager.trigger_event(
            "on_pre_draw_cards", pre_draw_event_data
        )

        self.hand.extend(["card"] * res["count"])

        post_draw_event_data = res
        res = self._event_manager.trigger_event(
            "on_post_draw_cards", post_draw_event_data
        )
