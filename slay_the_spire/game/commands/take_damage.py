from .command import Command


class TakeDamage(Command):
    def __init__(self, amount):
        self.amount = amount

    def invoke(self, event_data, target):
        target.take_damage(self.amount, self)
