from effect_system import Effect

from . import *
from ..game.relics import Relic


def test_relic_init():
		relic = Relic("test_relic")
		assert relic.name == "test_relic"
		assert len(relic.stats) == 0
		assert len(relic.effects) == 0

def test_add_effect_to_relic():
		class TestEffect():
				def activate(self):
						pass

		relic = Relic("test_relic")
		effect = TestEffect()
		res = relic.add_effect(effect)

		assert res == relic
		assert len(relic.effects) == 1
		assert relic.effects[0] == effect
