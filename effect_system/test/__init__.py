import pytest
from ..content.event_manager import *


@pytest.fixture(autouse=True)
def event_manager():
    event_manager = EventManager()
    event_manager.reset()
    return EventManager()
