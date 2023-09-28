from effect_system import Effect, EventTrigger

from . import *
from ..game.relic import Relic


def test_relic_init():
		relic = Relic("test relic")
		assert relic.name == "test relic"
		assert len(relic.stats) == 0
		assert len(relic.effects) == 0

def test_add_effect_to_relic():
		class TestEffect(Effect):
				def activate(self):
						pass

		relic = Relic("test relic")
		effect = TestEffect()
		res = relic.add_effect(effect)

		assert res == relic
		assert len(relic.effects) == 1
		assert relic.effects[0] == effect

def test_relic_effects_active_after_equip():
		class TestEffect(Effect):
				def activate(self):
						pass

		relic = Relic("test relic")
		effect = TestEffect()
		trigger = EventTrigger("event_name")
		relic.add_effect(effect.set_trigger(trigger))
		relic.on_equip()
		assert trigger._is_armed == True
