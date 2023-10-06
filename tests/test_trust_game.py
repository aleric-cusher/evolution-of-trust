import pytest
from trust.trust_game import play_game, TrustGameActions
from trust.player import AlwaysCooperate

def test_p1_cheat_p2_cheat():
    player1_outcome, player2_outcome = play_game(TrustGameActions.CHEAT, TrustGameActions.CHEAT)
    assert player1_outcome == 0
    assert player2_outcome == 0

def test_p1_cheat_p2_cooperate():
    player1_outcome, player2_outcome = play_game(TrustGameActions.CHEAT, TrustGameActions.COOPERATE)
    assert player1_outcome == 3
    assert player2_outcome == -1

def test_p1_cooperate_p2_cheat():
    player1_outcome, player2_outcome = play_game(TrustGameActions.COOPERATE, TrustGameActions.CHEAT)
    assert player1_outcome == -1
    assert player2_outcome == 3

def test_p1_cooperate_p2_cooperate():
    player1_outcome, player2_outcome = play_game(TrustGameActions.COOPERATE, TrustGameActions.COOPERATE)
    assert player1_outcome == 2
    assert player2_outcome == 2

def test_always_cooperate_10_games():
    player1, player2 = AlwaysCooperate(), AlwaysCooperate()
    for _ in range(10):
        player1_outcome, player2_outcome = play_game(player1.action(), player2.action())
        player1.score += player1_outcome
        player2.score += player2_outcome
    assert player1.score == 20
    assert player2.score == 20
