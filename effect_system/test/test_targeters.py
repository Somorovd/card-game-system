from ..content.targeters import EventDataPropertyTargeter


def test_event_data_targeter():
    x_targeter = EventDataPropertyTargeter("x")
    event_data1 = {}
    event_data2 = {"x": "testing"}
    targets1 = x_targeter.get_targets(event_data1)
    targets2 = x_targeter.get_targets(event_data2)
    assert len(targets1) == 0
    assert len(targets2) == 1
    assert targets2[0] == "testing"
