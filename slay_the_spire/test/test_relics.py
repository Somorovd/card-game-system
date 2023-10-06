from effect_system import Effect, EventTrigger

from . import *
from ..game.relics import *
from ..game.card import Card, CardType
from ..game.card_manager import CardLocation


@pytest.fixture
def players():
    return [Player("jay"), Player("larry")]


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


def test_burning_blood(event_manager, game_manager):
    player = game_manager.player
    player.equip_relic(BurningBlood())
    player.take_damage(50, None)
    event_manager.trigger_event("on_combat_end", {})
    assert player.get_stat("health") == 56


def test_akabako(event_manager, players):
    jay, larry = players
    jay.equip_relic(Akabako())

    event_manager.trigger_event("on_combat_start", {})
    jay.attack(larry, 2)
    assert larry.get_stat("health") == 90
    jay.attack(larry, 2)
    assert larry.get_stat("health") == 88
    event_manager.trigger_event("on_combat_start", {})
    jay.attack(larry, 2)
    assert larry.get_stat("health") == 78


def test_bronze_scales(event_manager, game_manager, players):
    jay, larry = players
    jay.equip_relic(BronzeScales())

    game_manager.enemies.append(larry)
    larry.attack(jay, 2)
    assert larry.get_stat("health") == 97

    karen = Player("karen")
    jay.take_damage(7, karen)
    assert karen.get_stat("health") == 100


def test_ring_of_the_snake(event_manager, card_manager, players):
    jay, larry = players
    jay.equip_relic(RingOfTheSnake())
    card_manager.draw = [None] * 10

    card_manager.draw_cards(1)
    assert len(card_manager.hand) == 1

    event_manager.trigger_event("on_combat_start", {})
    card_manager.draw_cards(1)
    assert len(card_manager.hand) == 4

    card_manager.draw_cards(1)
    assert len(card_manager.hand) == 5

    event_manager.trigger_event("on_combat_start", {})
    card_manager.draw_cards(1)
    assert len(card_manager.hand) == 8


def test_centennial_puzzle(event_manager, card_manager, players):
    jay, larry = players
    game_manager.player = jay
    jay.equip_relic(CentennialPuzzle())
    card_manager.draw = [None] * 10

    larry.attack(jay, 4)
    assert len(card_manager.hand) == 0

    event_manager.trigger_event("on_combat_start", {})
    larry.attack(jay, 0)
    assert len(card_manager.hand) == 0

    larry.attack(jay, 2)
    assert len(card_manager.hand) == 3

    larry.attack(jay, 2)
    assert len(card_manager.hand) == 3

    event_manager.trigger_event("on_combat_start", {})
    larry.attack(jay, 2)
    assert len(card_manager.hand) == 6


def test_maw_bank(event_manager, game_manager, players):
    jay, larry = players
    game_manager.player = jay
    jay.equip_relic(MawBank())

    event_manager.trigger_event("on_player_climb_floor", {})
    assert jay.get_stat("gold") == 12

    event_manager.trigger_event("on_player_climb_floor", {})
    event_manager.trigger_event("on_player_climb_floor", {})
    assert jay.get_stat("gold") == 36

    event_manager.trigger_event("on_player_shop_purchase", {})
    event_manager.trigger_event("on_player_climb_floor", {})
    assert jay.get_stat("gold") == 36


def test_strawberry(event_manager, game_manager, players):
    jay, larry = players
    game_manager.player = jay

    assert jay.get_stat("max_health") == 100
    jay.equip_relic(Strawberry())
    assert jay.get_stat("max_health") == 107
    jay.equip_relic(Relic("dummy"))
    assert jay.get_stat("max_health") == 107


def test_the_boot(event_manager, players):
    jay, larry = players
    jay.equip_relic(TheBoot())

    event_data = {"amount": 2}
    res = event_manager.trigger_event("on_enemy_pre_take_damage", event_data)
    assert res["amount"] == 5


def test_toy_ornithopter(event_manager, game_manager, players):
    jay, larry = players
    game_manager.player = jay

    jay.take_damage(50, None)
    assert jay.get_stat("health") == 50
    jay.drink_potion(None)
    assert jay.get_stat("health") == 50
    jay.equip_relic(ToyOrnithopter())
    jay.drink_potion(None)
    assert jay.get_stat("health") == 55


def test_art_of_war(event_manager, game_manager, card_manager, players, test_listener):
    jay, larry = players
    game_manager.player = jay

    attack_card = Card("attack", CardType.ATTACK, 0)
    power_card = Card("attack", CardType.POWER, 0)
    card_manager.hand = [attack_card, power_card]

    jay.equip_relic(ArtOfWar())
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)
    card_manager.play_card(power_card, to_location=CardLocation.HAND)
    assert jay.get_stat("energy") == 3

    event_manager.trigger_event("on_player_start_turn", {})
    event_manager.trigger_event("on_player_end_turn", {})
    assert jay.get_stat("energy") == 4

    test_listener.create_listener("on_post_play_card")

    event_manager.trigger_event("on_player_start_turn", {})
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)
    assert len(test_listener.events) == 1
    assert test_listener.events[0][1].get("type") == CardType.ATTACK

    event_manager.trigger_event("on_player_end_turn", {})
    assert jay.get_stat("energy") == 4


def test_ceramic_fish(game_manager, card_manager, players):
    jay, larry = players
    game_manager.player = jay

    card = Card("card", CardType.ATTACK, 0)
    card_manager.add_card(card, CardLocation.DECK)
    assert jay.get_stat("gold") == 0

    jay.equip_relic(CeramicFish())
    card = Card("card", CardType.ATTACK, 0)
    card_manager.add_card(card, CardLocation.DECK)
    card_manager.add_card(card, CardLocation.DECK)
    assert jay.get_stat("gold") == 18


def test_happy_flower(event_manager, game_manager, players):
    jay, larry = players
    game_manager.player = jay

    jay.equip_relic(HappyFlower())
    event_manager.trigger_event("on_player_start_turn", {})
    assert jay.get_stat("energy") == 3
    event_manager.trigger_event("on_player_start_turn", {})
    assert jay.get_stat("energy") == 3
    event_manager.trigger_event("on_player_start_turn", {})
    assert jay.get_stat("energy") == 4
    event_manager.trigger_event("on_player_start_turn", {})
    assert jay.get_stat("energy") == 4
    event_manager.trigger_event("on_player_start_turn", {})
    assert jay.get_stat("energy") == 4
    event_manager.trigger_event("on_player_start_turn", {})
    assert jay.get_stat("energy") == 5


def test_nunchaku(event_manager, game_manager, card_manager, players):
    jay, larry = players
    game_manager.player = jay

    jay.equip_relic(Nunchaku())
    attack_card = Card("attack", CardType.ATTACK, 0)
    power_card = Card("attack", CardType.POWER, 0)
    card_manager.hand = [attack_card, power_card]

    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 1
    card_manager.play_card(power_card, to_location=CardLocation.HAND)
    assert jay.get_stat("energy") == 3
    card_manager.play_card(power_card, to_location=CardLocation.HAND)
    card_manager.play_card(power_card, to_location=CardLocation.HAND)
    card_manager.play_card(power_card, to_location=CardLocation.HAND)
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 2
    assert jay.get_stat("energy") == 3
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 3
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 4
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 5
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 6
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 7
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 8
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 9
    assert jay.get_stat("energy") == 3
    card_manager.play_card(attack_card, to_location=CardLocation.HAND)  # 10
    assert jay.get_stat("energy") == 4


def test_omamori(card_manager, players):
    jay, larry = players
    curse = Card("curse", CardType.CURSE, 0)

    jay.equip_relic(Omamori())
    card_manager.add_card(curse, CardLocation.DECK)
    assert len(card_manager.deck) == 0
    card_manager.add_card(curse, CardLocation.DECK)
    assert len(card_manager.deck) == 0
    card_manager.add_card(curse, CardLocation.DECK)
    assert len(card_manager.deck) == 1


def test_pen_nib(event_manager, players):
    jay, larry = players

    jay.equip_relic(PenNib())

    jay.attack(larry, 1)  # 1
    assert larry.get_stat("health") == 99
    jay.attack(larry, 1)  # 2
    jay.attack(larry, 1)  # 3
    jay.attack(larry, 1)  # 4
    jay.attack(larry, 1)  # 5
    jay.attack(larry, 1)  # 6
    jay.attack(larry, 1)  # 7
    jay.attack(larry, 1)  # 8
    jay.attack(larry, 1)  # 9
    assert larry.get_stat("health") == 91
    jay.attack(larry, 1)  # 10
    assert larry.get_stat("health") == 89
    jay.attack(larry, 1)
    assert larry.get_stat("health") == 88


def test_bag_of_preparation(event_manager, players, card_manager):
    jay, larry = players
    jay.equip_relic(BagOfPreparation())
    card_manager.draw = [Card("", None, None)] * 20

    card_manager.draw_cards(2)
    assert len(card_manager.hand) == 2

    event_manager.trigger_event("on_combat_start", {})
    card_manager.draw_cards(2)
    assert len(card_manager.hand) == 6

    event_manager.trigger_event("on_combat_start", {})
    card_manager.draw_cards(0)
    assert len(card_manager.hand) == 8

    event_manager.trigger_event("on_combat_start", {})
    event_manager.trigger_event("on_player_turn_end", {})
    card_manager.draw_cards(2)
    assert len(card_manager.hand) == 10
