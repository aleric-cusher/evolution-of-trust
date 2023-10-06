import pytest
from trust.trust_game import play_game, TrustGameActions

def test_cheat_cheat():
    player1_outcome, player2_outcome = play_game(TrustGameActions.CHEAT, TrustGameActions.CHEAT)
    assert player1_outcome == 0
    assert player2_outcome == 0

def test_cheat_cooperate():
    player1_outcome, player2_outcome = play_game(TrustGameActions.CHEAT, TrustGameActions.COOPERATE)
    assert player1_outcome == 3
    assert player2_outcome == -1
