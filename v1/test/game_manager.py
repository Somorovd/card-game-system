from test import *


def test_create_subject():
    subject = Subject()
    assert len(subject._listeners.keys()) == 0
    assert len(subject._to_remove.keys()) == 0
    assert subject._is_notifying == False


def test_listener_added_to_subject():
    subject = Subject()
    event_name = "test1"
    update_func = lambda: None
    subject.add_listener(event_name, update_func)

    assert event_name in subject._listeners
    assert len(subject._listeners) == 1
    assert subject._listeners[event_name][0] == update_func


def test_listener_triggered():
    class A:
        def __init__(self):
            self.val = 0

    def update_func(event_data):
        event_data["A"].val = event_data["val"]

    subject = Subject()
    event_name = "test1"
    subject.add_listener(event_name, update_func)
    a = A()
    event_data = {"A": a, "val": 1901}
    subject.trigger_event(event_name, event_data)

    assert a.val == 1901
    assert event_name in subject._listeners
    assert len(subject._listeners) == 1
    assert subject._listeners[event_name][0] == update_func


def test_remove_listener():
    class A:
        def __init__(self):
            self.val = 0

    def update_func(event_data):
        event_data["A"].val = event_data["val"]

    subject = Subject()
    event_name = "test1"
    subject.add_listener(event_name, update_func)
    subject.remove_listener(event_name, update_func)
    a = A()
    event_data = {"A": a, "val": 1901}
    subject.trigger_event(event_name, event_data)

    assert a.val == 0
    assert not event_name in subject._listeners
    assert len(subject._listeners) == 0
