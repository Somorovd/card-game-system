from test import *


def test_stat_modifier_effect(players):
    jay = players["jay"]
    assert jay.get_stat("max_health") == 100
    assert len(jay.stats["max_health"].sources) == 0

    class JayTargeter(Targeter):
        def get_targets(self, effect, event_data):
            return [jay]

    stat_mod = StatModifierEffect("max_health", 3)
    stat_mod.add_targeters(JayTargeter())
    relic = Relic("").add_effect("on_event", stat_mod)
    assert len(relic.stats["max_health"].sources) == 1
    assert stat_mod in relic.stats["max_health"].sources
    assert relic.stats["max_health"].sources[stat_mod] == 0

    jay.add_relic(relic)
    assert len(jay.stats["max_health"].sources) == 1
    assert relic in jay.stats["max_health"].sources
    assert jay.stats["max_health"].sources[relic] == 0

    stat_mod.activate({})
    assert jay.get_stat("max_health") == 103
    stat_mod.activate({})
    assert jay.get_stat("max_health") == 106

    GAME_MANAGER.trigger_event("on_event", {})
    assert jay.get_stat("max_health") == 109
