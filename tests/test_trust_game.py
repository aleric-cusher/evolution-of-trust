import pytest
from trust.trust_game import play_game, TrustGameActions

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
