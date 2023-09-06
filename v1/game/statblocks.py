class PlayerStatBlock:
    def __init__(self, is_modifier=False):
        self.health = 10 if not is_modifier else 0
        self.power = 2 if not is_modifier else 0
