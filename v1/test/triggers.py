from test import *


def test_event_trigger(game_manager):
    event_name = "event1"
    validator = PropertyEquals("x", 12)
    trigger = EventTrigger(event_name, validator, game_manager=game_manager)
    assert trigger.event_name == event_name
    assert len(trigger.validators) == 1
    assert trigger.validators[0] == validator

    event_data1 = {"val": 6}
    event_data2 = {"val": 6, "x": 12}
    res1 = trigger.validate_event(event_data1)
    res2 = trigger.validate_event(event_data2)
    assert res1 == False
    assert res2 == True

    class TriggerParent:
        def __init__(self):
            self.val = 0

        def update(self, event_name, event_data):
            self.val += event_data["val"]

    parent = TriggerParent()
    trigger.set_parent(parent)
    assert trigger.parent == parent

    trigger.arm()
    assert len(game_manager._listeners) == 1
    assert event_name in game_manager._listeners

    game_manager.trigger_event(event_name, event_data2)
    assert parent.val == 6
