from test import *


@pytest.fixture
def test_effect(game_manager):
    class TestEffect(Effect):
        def activate(self, event_data, *target):
            target = target[0] if target else event_data["object"]
            target.val = event_data["val"]

    return TestEffect(game_manager=game_manager)


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


def test_effect_add_validators(test_effect):
    event_name1 = "test1"
    validator1 = PropertyEquals("x", 2)
    test_effect.set_event_validator(event_name1, validator1)
    assert len(test_effect._event_validators) == 1
    assert event_name1 in test_effect._event_validators
    assert len(test_effect._event_validators[event_name1]) == 1
    assert test_effect._event_validators[event_name1][0] == validator1

    event_name2 = "test2"
    test_effect.set_event_validator(event_name2, validator1)
    assert event_name1 in test_effect._event_validators
    assert event_name2 in test_effect._event_validators

    validator2 = PropertyEquals("y", 4)
    validator3 = PropertyEquals("z", 14)
    test_effect.set_event_validator(event_name1, validator2, validator3)
    assert len(test_effect._event_validators[event_name1]) == 2
    assert test_effect._event_validators[event_name1][0] == validator2
    assert test_effect._event_validators[event_name1][1] == validator3


def test_effect_activate_with_validators(test_effect, test_object):
    event_name = "test"
    validator1 = PropertyEquals("x", 2)
    validator2 = PropertyEquals("y", 4)

    test_effect.set_event_validator(event_name, validator1, validator2)
    event_data = {"object": test_object, "val": 23, "x": 2}
    test_effect.update(event_name, event_data)
    assert test_object.val == 0

    event_data["y"] = 4
    test_effect.update(event_name, event_data)
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


def test_triggers_off_events(game_manager, test_effect, test_object):
    class ObjectTargeter:
        def get_targets(self, event_data):
            return [test_object]

    targeter1 = ObjectTargeter()
    event_name = "event1"
    event_data = {"val": 30}
    test_effect.set_event_validator(event_name).add_targeter(targeter1)
    assert test_effect._is_listening == False

    test_effect.set_listening(True)
    assert test_effect._is_listening == True
    assert len(game_manager._listeners) == 1
    assert event_name in game_manager._listeners
    assert game_manager._listeners[event_name][0] == test_effect.update

    game_manager.trigger_event(event_name, event_data)
    assert test_object.val == 30


# def test_stat_modifier_effect(players):
#     jay = players["jay"]
#     assert jay.get_stat("max_health") == 100
#     assert len(jay.stats["max_health"].sources) == 0

#     class JayTargeter(Targeter):
#         def get_targets(self, effect, event_data):
#             return [jay]

#     stat_mod = StatModifierEffect("max_health", 3)
#     stat_mod.add_targeters(JayTargeter())
#     relic = Relic("").add_effect("on_event", stat_mod)
#     assert len(relic.stats["max_health"].sources) == 1
#     assert stat_mod in relic.stats["max_health"].sources
#     assert relic.stats["max_health"].sources[stat_mod] == 0

#     jay.add_relic(relic)
#     assert len(jay.stats["max_health"].sources) == 1
#     assert relic in jay.stats["max_health"].sources
#     assert jay.stats["max_health"].sources[relic] == 0

#     stat_mod.activate({})
#     assert jay.get_stat("max_health") == 103
#     stat_mod.activate({})
#     assert jay.get_stat("max_health") == 106

#     GAME_MANAGER.trigger_event("on_event", {})
#     assert jay.get_stat("max_health") == 109
