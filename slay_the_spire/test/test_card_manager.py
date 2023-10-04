from . import *
from ..game.card import Card, CardType
from ..game.card_manager import CardLocation


def test_reset(card_manager):
    card_manager.hand = [1, 2, 3, 4, 5]
    card_manager.reset()
    assert len(card_manager.hand) == 0


def test_add_remove_cards(card_manager):
    card1 = Card("1", None, None)
    card2 = Card("1", None, None)
    card3 = Card("1", None, None)
    card4 = Card("1", None, None)
    card_manager.add_card(card1, CardLocation.DECK)
    card_manager.add_card(card2, CardLocation.DECK)
    card_manager.add_card(card3, CardLocation.DECK)
    card_manager.add_card(card4, CardLocation.DECK)

    assert len(card_manager.deck) == 4
    assert card_manager.deck[0] == card1
    assert card_manager.deck[1] == card2
    assert card_manager.deck[2] == card3
    assert card_manager.deck[3] == card4

    card_manager.remove_card(card2, CardLocation.DECK)
    assert len(card_manager.deck) == 3
    assert not card2 in card_manager.deck


def test_add_cards_events(card_manager, test_listener):
    attack_card = Card("1", CardType.ATTACK, 1)
    test_listener.create_listener("on_pre_add_card")
    test_listener.create_listener("on_post_add_card")
    card_manager.add_card(attack_card, CardLocation.HAND)
    assert len(test_listener.events) == 2
    assert test_listener.events[0][0] == "on_pre_add_card"
    assert test_listener.events[1][0] == "on_post_add_card"

    pre_add_data = test_listener.events[0][1]
    post_add_data = test_listener.events[1][1]
    assert pre_add_data["card"] == attack_card
    assert pre_add_data["type"] == CardType.ATTACK
    assert pre_add_data["cost"] == 1
    assert pre_add_data["location"] == CardLocation.HAND
    assert post_add_data["card"] == attack_card
    assert post_add_data["type"] == CardType.ATTACK
    assert post_add_data["cost"] == 1
    assert post_add_data["location"] == CardLocation.HAND


def test_remove_card_events(card_manager, test_listener):
    skill_card = Card("1", CardType.SKILL, 3)
    card_manager.add_card(skill_card, CardLocation.DECK)
    test_listener.create_listener("on_pre_remove_card")
    test_listener.create_listener("on_post_remove_card")
    card_manager.remove_card(skill_card, CardLocation.DECK)
    assert len(test_listener.events) == 2
    assert test_listener.events[0][0] == "on_pre_remove_card"
    assert test_listener.events[1][0] == "on_post_remove_card"

    pre_remove_data = test_listener.events[0][1]
    post_remove_data = test_listener.events[1][1]
    assert pre_remove_data["card"] == skill_card
    assert pre_remove_data["type"] == CardType.SKILL
    assert pre_remove_data["cost"] == 3
    assert pre_remove_data["location"] == CardLocation.DECK
    assert post_remove_data["card"] == skill_card
    assert post_remove_data["type"] == CardType.SKILL
    assert post_remove_data["cost"] == 3
    assert post_remove_data["location"] == CardLocation.DECK


def test_draw_cards_full_deck(card_manager, test_listener):
    test_listener.create_listener("on_pre_draw_cards")
    test_listener.create_listener("on_post_draw_cards")

    card1 = Card("1", None, None)
    card2 = Card("2", None, None)
    card3 = Card("3", None, None)
    card_manager.add_card(card1, CardLocation.DRAW)
    card_manager.add_card(card2, CardLocation.DRAW)
    card_manager.add_card(card3, CardLocation.DRAW)

    card_manager.draw_cards(2)
    assert len(card_manager.hand) == 2
    assert len(card_manager.draw) == 1
    assert card_manager.hand[0] == card1
    assert card_manager.hand[1] == card2
    assert card_manager.draw[0] == card3

    assert len(test_listener.events) == 2
    assert test_listener.events[0][0] == "on_pre_draw_cards"
    assert test_listener.events[1][0] == "on_post_draw_cards"

    pre_draw_data = test_listener.events[0][1]
    post_draw_data = test_listener.events[1][1]

    assert pre_draw_data["count"] == 2
    assert post_draw_data["count"] == 2
    assert card1 in post_draw_data["cards"]
    assert card2 in post_draw_data["cards"]
