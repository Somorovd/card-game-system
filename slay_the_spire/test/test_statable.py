from . import *
from ..game.statable import Statable, Stat
from effect_system import Subject

def test_statble_init():
	statable = Statable()
	assert isinstance(statable, Subject)
	assert len(statable._listeners) == 0
	assert isinstance(statable.stats, dict)
	assert len(statable.stats) == 0

def test_stat_init():
	stat1 = Stat("type1", 10,)
	stat2 = Stat("type2", 11, current=4)
	assert isinstance(stat1, Subject)
	assert len(stat1._listeners) == 0
	assert stat1.stat_type == "type1"
	assert stat2.stat_type == "type2"
	assert stat1.base == 10
	assert stat2.base == 11
	assert stat1.current == 10
	assert stat2.current == 4
	assert stat1.mod == 0
	assert stat2.mod == 0
	assert len(stat1.sources) == 0
	assert len(stat2.sources) == 0

def test_stat_adjustments():
	stat = Stat("type", 20, current=2)
	stat.adjust_current(4)
	assert stat.current == 6
	stat.reset_current()
	assert stat.current == 20

def test_stat_sources():
	stat = Stat("type", 20, current=2)

	with pytest.raises(TypeError):
		source = "source"
		stat.add_source(source)

	source = Stat("source", 3)
	stat.add_source(source)
	stat_event = "on_stat_update"
	assert len(stat.sources) == 1
	assert source in stat.sources
	assert stat.sources[source] == 0
	assert len(source._listeners) == 1
	assert stat_event in source._listeners
	assert len(source._listeners[stat_event]) == 1

	stat.update_source(source, 5)
	assert stat.mod == 5
	assert stat.current == 7
	assert stat.sources[source] == 5

	stat.reset_current()
	assert stat.current == 25

	source.trigger_event(stat_event, {})
	source.trigger_event(stat_event, {"stat_type": "other", "amount": 5})
	source.trigger_event(stat_event, {"stat_type": "type", "value": 5})
	assert stat.mod == 5
	source.trigger_event(stat_event, {"stat_type": "type", "amount": 5})
	assert stat.mod == 10
	assert stat.current == 30
	assert stat.sources[source] == 10

	source2 = Stat("type", 0)
	stat.add_source(source2)
	assert len(stat.sources) == 2
	assert source2 in stat.sources

	source2.trigger_event(stat_event, {"stat_type": "type", "amount": 2})
	assert stat.mod == 12
	assert stat.current == 32
	assert stat.sources[source] == 10
	assert stat.sources[source2] == 2

	# # source stat_type is not the same
	source._trigger_update(2)
	assert stat.mod == 12
	source2._trigger_update(2)
	assert stat.mod == 14

	source2.adjust_current(2)
	assert stat.mod == 16

	source3 = Stat("type", 0)
	source2.add_source(source3)
	source3.adjust_current(2)
	assert stat.mod == 18
