import pytest
from game import *


@pytest.fixture
def players():
    jay = Player("Jay")
    jay.stats["health"] = Stat("health", 10)
    jay.stats["max_health"] = Stat("max_health", 100)
    larry = Player("Larry")
    larry.stats["health"] = Stat("health", 10)
    larry.stats["max_health"] = Stat("max_health", 100)
    return {"jay": jay, "larry": larry}
