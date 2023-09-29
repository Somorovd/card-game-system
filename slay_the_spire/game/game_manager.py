class GameManager:
    _instance = None

    def __new__(cls):
        if cls._instance:
            return cls._instance
        else:
            cls._instance = super(GameManager, cls).__new__(cls)
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        super().__init__()
        self._initialized = True
        self.player = None
        self.enemies = []

    def reset(self):
        super().__init__()
