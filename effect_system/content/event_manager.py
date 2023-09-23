from .subject import Subject


class EventManager(Subject):
    def __init__(self):
        super().__init__()

    @classmethod
    def set_global_manager(self, event_manager):
        EVENT_MANAGER = event_manager


EVENT_MANAGER = EventManager()
