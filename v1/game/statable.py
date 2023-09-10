from .game_manager import Subject


class Statable(Subject):
    def __init__(self):
        super().__init__()
        self.stats = {}

    def add_stat_modifier(self, stat_type, source):
        if not stat_type in self.stats:
            raise TypeError(f"{self} has no stat '{stat_type}'")
        if not issubclass(type(source), Subject):
            raise TypeError("Modifier source must implament Subject interface")

        stat = self.stats[stat_type]
        stat.add_source(source)

        def _update_func(event_data):
            if event_data["stat"] != stat_type:
                return

            prev = stat.current
            stat.update_source(source, event_data["amount"])
            current = stat.current
            print(f"{stat_type} updated from {prev} to {current}")
            stat_update_event_data = {"stat": stat_type, "amount": current}
            self.trigger_event("on_stat_update", stat_update_event_data)

        source.add_listener("on_stat_update", _update_func)


class Stat:
    def __init__(self, base, current=None):
        self.base = base
        self.current = current or base
        self.mod = 0
        self.sources = {}

    def add_source(self, source):
        self.sources[source] = 0

    def update_source(self, source, amount):
        diff = amount - self.sources[source]
        self.mod += diff
        self.current += diff
        self.sources[source] = amount
