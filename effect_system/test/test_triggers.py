import pytest
from . import *
from ..content.triggers import *
from ..content.validators import PropertyEquals


@pytest.fixture()
def trigger_parent():
    class TriggerParent:
        def __init__(self):
            self.val = 0

        def update(self, event_data, trigger=None):
            self.val = event_data["val"]

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

    trigger.reset()
    assert trigger._is_armed == False


def test_sequence_trigger(event_manager, trigger_parent):
    event_name1 = "event1"
    event_name2 = "event2"
    restart_event = "reset"
    trigger1 = EventTrigger(event_name1)
    trigger2 = EventTrigger(event_name2)
    restart_trigger = EventTrigger(restart_event)

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

    sequence.add_restart(restart_trigger)
    assert len(sequence._triggers) == 2
    assert sequence._restart_trigger == restart_trigger
    assert trigger1._is_armed == False
    assert trigger2._is_armed == False
    assert restart_trigger._is_armed == False
    assert restart_trigger._parent == sequence

    sequence.arm()
    assert sequence._is_armed == True
    assert sequence._triggers[0]._is_armed == True
    assert sequence._triggers[1]._is_armed == False
    assert sequence._restart_trigger._is_armed == True

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

    sequence.reset()
    assert sequence._is_armed == False
    assert all([t._is_armed == False for t in sequence._triggers]) == True
    assert sequence._pos == 0
    assert len(sequence._triggers) == 4

    sequence.arm()
    event_manager.trigger_event(event_name1, {})
    event_manager.trigger_event(event_name2, {})
    event_manager.trigger_event(restart_event, {})
    assert sequence._pos == 0
    assert sequence._triggers[0]._is_armed == True

    sequence.disarm()
    assert sequence._is_armed == False
    assert all([t._is_armed == False for t in sequence._triggers]) == True
    assert sequence._restart_trigger._is_armed == False

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
    assert toggle._toggled == False
    assert toggle._init_toggled == False
    assert trigger_on._parent == toggle
    assert trigger_off._parent == toggle
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False

    toggle.arm()
    assert toggle._is_armed == True
    assert trigger_on._is_armed == True
    assert trigger_off._is_armed == False
    assert toggle._toggled == False

    toggle.toggle_on()
    assert toggle._toggled == True
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == True

    toggle.disarm()
    assert toggle._is_armed == False
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False
    assert toggle._toggled == True

    toggle.arm()
    assert toggle._is_armed == True
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == True
    assert toggle._toggled == True

    toggle.set_init_toggled(True)
    assert toggle._init_toggled == True
    assert toggle._toggled == True

    toggle.reset()
    assert toggle._is_armed == False
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False
    assert toggle._toggled == True

    toggle.set_init_toggled(False)
    assert toggle._init_toggled == False
    assert toggle._toggled == False

    toggle.arm()
    toggle.reset()
    assert toggle._is_armed == False
    assert trigger_on._is_armed == False
    assert trigger_off._is_armed == False
    assert toggle._toggled == False

    toggle.set_trigger(event_trigger)
    assert toggle._trigger == event_trigger
    assert event_trigger._parent == toggle
    assert event_trigger._is_armed == False

    toggle.arm()
    assert event_trigger._is_armed == False

    toggle.toggle_on()
    assert event_trigger._is_armed == True

    event_manager.trigger_event(event_off, {})
    assert trigger_on._is_armed == True
    assert trigger_off._is_armed == False
    assert event_trigger._is_armed == False
    assert toggle._toggled == False

    event_manager.trigger_event(event_name1, {"val": 21})
    assert trigger_parent.val == 0

    event_manager.trigger_event(event_on, {})
    event_manager.trigger_event(event_name1, {"val": 95})
    assert trigger_parent.val == 95


def test_repeat_trigger(event_manager, trigger_parent):
    event_name = "repeating"
    event_trigger = EventTrigger(event_name)
    repeat_count = 3

    repeat_trigger = Repeat(event_trigger, repeat_count)
    repeat_trigger.set_parent(trigger_parent)
    assert repeat_trigger._trigger == event_trigger
    assert event_trigger._parent == repeat_trigger
    assert repeat_trigger._max_count == repeat_count
    assert repeat_trigger._count == 0

    repeat_trigger.arm()
    assert repeat_trigger._is_armed == True
    assert event_trigger._is_armed == True

    repeat_trigger.disarm()
    assert repeat_trigger._is_armed == False
    assert event_trigger._is_armed == False

    repeat_trigger.arm()
    event_manager.trigger_event(event_name, {"val": 1})
    assert repeat_trigger._count == 1
    assert trigger_parent.val == 0

    event_manager.trigger_event("other", {"val": 2})
    assert repeat_trigger._count == 1
    assert trigger_parent.val == 0

    event_manager.trigger_event(event_name, {"val": 3})
    assert repeat_trigger._count == 2
    assert trigger_parent.val == 0

    repeat_trigger.reset()
    assert repeat_trigger._is_armed == False
    assert repeat_trigger._count == 0

    repeat_trigger.arm()
    event_manager.trigger_event(event_name, {"val": 10})
    event_manager.trigger_event(event_name, {"val": 20})
    event_manager.trigger_event(event_name, {"val": 30})
    assert repeat_trigger._count == 0
    assert trigger_parent.val == 30


def test_n_times_trigger(event_manager, trigger_parent):
    event_name = "event"
    event_trigger = EventTrigger(event_name)
    event_count = 3
    ntimes = NTimes(event_trigger, event_count)
    ntimes.set_parent(trigger_parent)

    assert ntimes._trigger == event_trigger
    assert ntimes._max_count == 3
    assert ntimes._count == 0
    assert ntimes._init_toggled == True
    assert event_trigger._parent == ntimes

    ntimes.arm()
    assert ntimes._is_armed == True
    assert event_trigger._is_armed == True

    event_manager.trigger_event(event_name, {"val": 10})
    assert trigger_parent.val == 10
    assert ntimes._count == 1

    event_manager.trigger_event(event_name, {"val": 20})
    assert trigger_parent.val == 20
    assert ntimes._count == 2

    event_manager.trigger_event(event_name, {"val": 40})
    assert trigger_parent.val == 40
    assert ntimes._count == 3
    assert ntimes._is_armed == False
    assert event_trigger._is_armed == False

    ntimes.arm()
    event_manager.trigger_event(event_name, {"val": 60})
    assert trigger_parent.val == 40
    assert ntimes._count == 3
    assert ntimes._is_armed == False
    assert event_trigger._is_armed == False

    ntimes.reset()
    assert ntimes._count == 0
    assert ntimes._is_armed == False
    assert event_trigger._is_armed == False

    ntimes.arm()
    event_manager.trigger_event(event_name, {"val": 60})
    assert trigger_parent.val == 60
    assert ntimes._count == 1
    assert ntimes._is_armed == True
    assert event_trigger._is_armed == True
