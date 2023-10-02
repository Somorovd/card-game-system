from . import *
from ..game.triggers import *
from effect_system import Effect


def test_on_equip_tigger(event_manager):
    class TestEffect(Effect):
        def __init__(self):
            super().__init__()
            self.val = 0

        def activate(self, event_data, target):
            self.val = event_data["val"]

    jay = Player("jay")
    effect = TestEffect()
    trigger = OnEquipTrigger()
    effect.set_trigger(trigger)
    trigger.arm()

    assert effect.val == 0

    event_manager.trigger_event("on_player_equip_relic", {"val": 10})
    assert effect.val == 10
    assert trigger._is_armed == False
