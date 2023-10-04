from . import *
from ..game.deck import Deck
from ..game.card import Card, CardType


def test_deck_init():
    deck = Deck()
    assert len(deck.cards) == 0


def test_deck_cards():
    deck = Deck()
    card1 = Card("1", None, None)
    card2 = Card("1", None, None)
    card3 = Card("1", None, None)
    card4 = Card("1", None, None)
    deck.add_card(card1)
    deck.add_card(card2)
    deck.add_card(card3)
    deck.add_card(card4)

    assert len(deck.cards) == 4
    assert deck.cards[0] == card1
    assert deck.cards[1] == card2
    assert deck.cards[2] == card3
    assert deck.cards[3] == card4

    deck.remove_card(card2)
    assert len(deck.cards) == 3
    assert not card2 in deck.cards
