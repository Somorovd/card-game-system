import pytest
from ..test import *
from ..content.triggers import *
from ..content.validators import PropertyEquals


@pytest.fixture()
def trigger_parent():
    class TriggerParent:
        def __init__(self):
            self.val = 0

        def update(self, event_data, trigger=None):
            self.val += event_data["val"]

    return TriggerParent()


def test_event_trigger(event_manager, trigger_parent):
    event_name = "event1"
    validator = PropertyEquals("x", 12)
    trigger = EventTrigger(event_name, validator)
    assert trigger._event_name == event_name
    assert len(trigger._validators) == 1
    assert trigger._validators[0] == validator

    event_data1 = {"val": 6}
    event_data2 = {"val": 6, "x": 12}
    res1 = trigger.validate_event(event_data1)
    res2 = trigger.validate_event(event_data2)
    assert res1 == False
    assert res2 == True

    trigger.set_parent(trigger_parent)
    assert trigger._parent == trigger_parent

    trigger.arm()
    assert len(event_manager._listeners) == 1
    assert event_name in event_manager._listeners

    event_manager.trigger_event(event_name, event_data2)
    assert trigger_parent.val == 6


def test_sequence_trigger(event_manager, trigger_parent):
    event_name1 = "event1"
    event_name2 = "event2"
    reset_event = "reset"
    trigger1 = EventTrigger(event_name1)
    trigger2 = EventTrigger(event_name2)
    reset_trigger = EventTrigger(reset_event)

    sequence = Sequence()
    assert len(sequence._triggers) == 0
    assert sequence._pos == 0
    assert sequence._is_armed == False

    sequence.set_parent(trigger_parent)
    assert sequence._parent == trigger_parent

    sequence.add_seq(trigger1)
    assert len(sequence._triggers) == 1
    assert sequence._triggers[0] == trigger1
    assert sequence._pos == 0
    assert trigger1._is_armed == False
    assert trigger1._parent == sequence

    sequence.add_seq(trigger2)
    assert len(sequence._triggers) == 2
    assert sequence._triggers[0] == trigger1
    assert sequence._triggers[1] == trigger2
    assert sequence._pos == 0
    assert trigger1._is_armed == False
    assert trigger2._is_armed == False
    assert trigger2._parent == sequence

    sequence.add_reset(reset_trigger)
    assert len(sequence._triggers) == 2
    assert sequence._reset == reset_trigger
    assert trigger1._is_armed == False
    assert trigger2._is_armed == False
    assert reset_trigger._is_armed == False
    assert reset_trigger._parent == sequence

    sequence.arm()
    assert sequence._is_armed == True
    assert sequence._triggers[0]._is_armed == True
    assert sequence._triggers[1]._is_armed == False
    assert sequence._reset._is_armed == True

    event_manager.trigger_event(event_name1, {})
    assert sequence._pos == 1
    assert sequence._triggers[0]._is_armed == False
    assert sequence._triggers[1]._is_armed == True

    event_manager.trigger_event(event_name2, {"val": 14})
    assert sequence._pos == 0
    assert sequence._triggers[0]._is_armed == True
    assert sequence._triggers[1]._is_armed == False
    assert trigger_parent.val == 14

    trigger3 = EventTrigger(event_name1)
    trigger4 = EventTrigger(event_name2)
    sequence.add_seq(trigger3).add_seq(trigger4)
    assert len(sequence._triggers) == 4

    event_manager.trigger_event(event_name1, {})
    event_manager.trigger_event(event_name2, {})
    assert sequence._pos == 2
    assert sequence._triggers[2]._is_armed == True

    event_manager.trigger_event(reset_event, {})
    assert sequence._pos == 0
    assert sequence._triggers[0]._is_armed == True

    sequence.disarm()
    assert sequence._is_armed == False
    assert all([t._is_armed == False for t in sequence._triggers]) == True
    assert sequence._reset._is_armed == False

    event_manager.trigger_event(event_name1, {})
    assert sequence._pos == 0
    assert all([t._is_armed == False for t in sequence._triggers]) == True


def test_toggle_trigger(event_manager, trigger_parent):
    event_on = "event_on"
    event_off = "event_off"
    event_name1 = "event1"
    trigger_on = EventTrigger(event_on)
    trigger_off = EventTrigger(event_off)
    event_trigger = EventTrigger(event_name1)

    toggle = Toggle()
    toggle.set_parent(trigger_parent)
    assert toggle._toggled == False

    toggle.set_toggle_on(trigger_on)
    toggle.set_toggle_off(trigger_off)
    assert toggle._toggle_on == trigger_on
    assert toggle._toggle_off == trigger_off
    assert trigger_on._parent == toggle
    assert trigger_off._parent == toggle
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False

    toggle.arm()
    assert toggle._is_armed == True
    assert trigger_on._is_armed == True
    assert trigger_off._is_armed == False

    toggle.disarm()
    assert toggle._is_armed == False
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False

    toggle.set_toggled(True)
    assert toggle._toggled == True
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False

    toggle.arm()
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == True

    toggle.set_toggled(False)
    assert toggle._toggled == False
    assert trigger_on._is_armed == True
    assert trigger_off._is_armed == False

    toggle.set_trigger(event_trigger)
    assert toggle._trigger == event_trigger
    assert event_trigger._parent == toggle
    assert event_trigger._is_armed == False

    toggle.set_toggled(True)
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == True
    assert event_trigger._is_armed == True

    event_manager.trigger_event(event_off, {})
    assert trigger_on._is_armed == True
    assert trigger_off._is_armed == False
    assert event_trigger._is_armed == False

    event_manager.trigger_event(event_name1, {"val": 21})
    assert trigger_parent.val == 0

    event_manager.trigger_event(event_on, {})
    event_manager.trigger_event(event_name1, {"val": 95})
    assert trigger_parent.val == 95

    toggle.disarm()
    assert toggle._is_armed == False
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False
    assert event_trigger._is_armed == False
