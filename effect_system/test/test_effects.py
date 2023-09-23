import pytest
from . import *
from ..content.effects import Effect
from ..content.targeters import EventDataPropertyTargeter
from ..content.triggers import EventTrigger
from ..content.validators import PropertyEquals


@pytest.fixture
def test_effect():
    class TestEffect(Effect):
        def activate(self, event_data, *target):
            target = target[0] if target else event_data["object"]
            target.val = event_data["val"]

    return TestEffect()


@pytest.fixture
def test_object():
    class TestObject:
        def __init__(self):
            self.val = 0

    return TestObject()


def test_effect_activate_no_validators(test_effect, test_object):
    event_data = {"object": test_object, "val": 10}
    test_effect.activate(event_data)
    assert test_object.val == 10


def test_effect_set_trigger(test_effect):
    event_name1 = "test1"
    validator1 = PropertyEquals("x", 2)
    test_effect.set_trigger(event_name1, validator1)
    assert test_effect._trigger._event_name == event_name1
    assert test_effect._trigger._validators[0] == validator1

    validator2 = PropertyEquals("y", 30)
    trigger = EventTrigger(event_name1, validator2)
    test_effect.set_trigger(trigger)
    assert test_effect._trigger == trigger
    assert trigger._parent == test_effect


def test_effect_activates_from_trigger(test_effect, test_object):
    event_name = "test"
    validator1 = PropertyEquals("x", 2)
    validator2 = PropertyEquals("y", 4)
    trigger = EventTrigger(event_name, validator1, validator2)

    test_effect.set_trigger(trigger)
    event_data = {"object": test_object, "val": 23, "x": 2}
    trigger.update(event_data)
    assert test_object.val == 0

    event_data["y"] = 4
    trigger.update(event_data)
    assert test_object.val == 23


def test_effect_add_targeter(test_effect):
    targeter1 = EventDataPropertyTargeter("prop")
    test_effect.add_targeter(targeter1)
    assert len(test_effect._targeters) == 1
    assert test_effect._targeters[0] == targeter1

    targeter2 = EventDataPropertyTargeter("test")
    test_effect.add_targeter(targeter2)
    assert len(test_effect._targeters) == 2
    assert test_effect._targeters[0] == targeter1
    assert test_effect._targeters[1] == targeter2


def test_effect_get_targets(test_effect):
    targeter1 = EventDataPropertyTargeter("prop")
    targeter2 = EventDataPropertyTargeter("test")
    event_data = {"prop": [1], "test": [5, 6], "other": [10, 11]}
    test_effect.add_targeter(targeter1).add_targeter(targeter2)
    targets = test_effect.get_targets(event_data)
    assert len(targets) == 3
    assert targets[0] == 1
    assert targets[1] == 5
    assert targets[2] == 6


def test_effect_apply_to_target(test_effect, test_object):
    class ObjectTargeter:
        def get_targets(self, event_data):
            return [test_object]

    targeter1 = ObjectTargeter()
    event_data = {"val": 30}
    test_effect.add_targeter(targeter1)
    test_effect.activate_on_targets(event_data)
    assert test_object.val == 30


def test_effect_triggers_off_events(event_manager, test_effect, test_object):
    class ObjectTargeter:
        def get_targets(self, event_data):
            return [test_object]

    targeter1 = ObjectTargeter()
    event_name = "event1"
    event_data = {"val": 30}
    test_effect.set_trigger(event_name).add_targeter(targeter1)
    test_effect.arm_trigger(True)
    assert test_effect._trigger._is_armed == True
    assert event_name in event_manager._listeners
    assert event_manager._listeners[event_name][0] == test_effect._trigger.update

    event_manager.trigger_event(event_name, event_data)
    assert test_object.val == 30
