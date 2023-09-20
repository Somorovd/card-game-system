import pytest
from game import *


@pytest.fixture
def players():
    jay = Player("Jay")
    jay.add_stat("health", 10)
    jay.add_stat("max_health", 100)
    larry = Player("Larry")
    larry.add_stat("health", 10)
    larry.add_stat("max_health", 100)
    return {"jay": jay, "larry": larry}
