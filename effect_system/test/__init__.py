import pytest
from ..content.event_manager import *


@pytest.fixture(autouse=True)
def event_manager():
    event_manager = EventManager()
    EventManager.set_global_manager(event_manager)
    return event_manager
