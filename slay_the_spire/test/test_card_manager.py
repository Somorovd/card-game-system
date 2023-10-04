from . import *


def test_reset(card_manager):
    card_manager.hand = [1, 2, 3, 4, 5]
    card_manager.reset()
    assert len(card_manager.hand) == 0


def test_draw_cards(card_manager, test_listener):
    test_listener.create_listener("on_pre_draw_cards")
    test_listener.create_listener("on_post_draw_cards")

    card_manager.draw_cards(2)
    assert len(card_manager.hand) == 2
    assert len(test_listener.events) == 2
    assert test_listener.events[0][0] == "on_pre_draw_cards"
    assert test_listener.events[1][0] == "on_post_draw_cards"

    pre_draw_data = test_listener.events[0][1]
    post_draw_data = test_listener.events[1][1]

    assert pre_draw_data["count"] == 2
    assert post_draw_data["count"] == 2
