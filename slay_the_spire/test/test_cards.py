from . import *
from ..game.card import Card, CardType
from ..game.effects import Heal, TakeDamage
from ..game.targeters import player_targeter, selected_enemy_targeter


def test_card_init():
    card = Card("card", CardType.ATTACK, 1)
    assert card.name == "card"
    assert card.type == CardType.ATTACK
    assert card.get_stat("cost") == 1
    assert len(card._effects) == 0


def test_add_effect_to_card():
    card = Card("heal", CardType.SKILL, 1)
    effect = Heal(2)
    res = card.add_effect(effect)
    assert res == card
    assert len(card._effects) == 1
    assert card._effects[0] == effect


def test_play_card(game_manager):
    jay = Player("jay")
    larry = Player("larry")
    game_manager.player = jay
    game_manager.selected_enemy = larry
    jay.take_damage(50, None)
    card = (
        Card("heal", CardType.SKILL, 1)
        .add_effect(Heal(2).add_targeter(player_targeter))
        .add_effect(TakeDamage(10).add_targeter(selected_enemy_targeter))
    )
    card.play()
    assert jay.get_stat("health") == 52
    assert larry.get_stat("health") == 90
