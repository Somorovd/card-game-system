from test import *


@pytest.fixture
def test_effect():
    class TestEffect(Effect):
        def activate(self, event_data):
            event_data["object"].val = event_data["val"]

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
