from effect_system import Subject

class Statable(Subject):
    def __init__(self):
        super().__init__()
        self.stats = {}

#     def add_stat(self, stat_type, base, current=None):
#         stat = Stat(stat_type, base, current=current)
#         self.stats[stat_type] = stat
#         stat.add_listener(
#             "on_stat_update",
#             lambda event_data: self.trigger_event("on_stat_update", event_data),
#         )

#     def has_stat(self, stat_type):
#         return stat_type in self.stats

#     def get_stat(self, stat_type):
#         return self.stats[stat_type].current

#     def adjust_stat(self, stat_type, amount):
#         self.stats[stat_type].adjust_current(amount)

#     def add_stat_source(self, stat_type, source):
#         if not stat_type in self.stats:
#             self.add_stat(stat_type, 0)

#         stat = self.stats[stat_type]
#         stat.add_source(source)


class Stat(Subject):
    def __init__(self, stat_type, base, current=None):
        super().__init__()
        self.stat_type = stat_type
        self.base = base
        self.current = current or base
        self.mod = 0
        self.sources = {}

    def adjust_current(self, amount):
        self.current += amount
        self._trigger_update(amount)

    def reset_current(self):
        self.current = self.base + self.mod

    def add_source(self, source):
        if not isinstance(source, Subject):
            raise(TypeError)
        self.sources[source] = 0

        def _update_func(event_data):
            if event_data.get("stat_type") != self.stat_type:
                return
            self.update_source(source, event_data.get("amount") or 0)

        source.add_listener("on_stat_update", _update_func)

    def update_source(self, source, amount):
        self.mod += amount
        self.current += amount
        self.sources[source] += amount
        self._trigger_update(amount)

    def _trigger_update(self, amount):
        stat_update_event_data = {"stat_type": self.stat_type, "amount": amount}
        self.trigger_event("on_stat_update", stat_update_event_data)
