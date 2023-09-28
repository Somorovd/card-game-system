import pytest
from effect_system import EventManager

@pytest.fixture(autouse=True)
def event_manager():
    event_manager = EventManager()
    event_manager.reset()
    return EventManager()

@pytest.fixture
def test_listener():
    class TestListener:
        def __init__(self):
          self._event_manager = EventManager()
          self.events = []

        def create_listener(self, event_name):
          self._event_manager.add_listener(
            event_name,
            lambda event_data: self.events.append((event_name, event_data.copy()))
          )
    return TestListener()
