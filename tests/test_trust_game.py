import pytest
from trust.trust_game import play_game
from trust.actions import TrustGameActions
from trust.player import AlwaysCooperate, Player

def mock_action_cheat():
    return TrustGameActions.CHEAT

def mock_action_cooperate():
    return TrustGameActions.COOPERATE

def test_invalid_inputs_to_play_game():
    with pytest.raises(TypeError):
        play_game('a', 4)

def test_p1_cheat_p2_cheat(monkeypatch):
    player1, player2 = Player(), Player()

    monkeypatch.setattr(player1, 'action', mock_action_cheat)
    monkeypatch.setattr(player2, 'action', mock_action_cheat)

    play_game(player1, player2)
    assert player1.score == 0
    assert player2.score == 0

def test_p1_cheat_p2_cooperate(monkeypatch):
    player1, player2 = Player(), Player()

    monkeypatch.setattr(player1, 'action', mock_action_cheat)
    monkeypatch.setattr(player2, 'action', mock_action_cooperate)

    play_game(player1, player2)
    assert player1.score == 3
    assert player2.score == -1

def test_p1_cooperate_p2_cheat(monkeypatch):
    player1, player2 = Player(), Player()

    monkeypatch.setattr(player1, 'action', mock_action_cooperate)
    monkeypatch.setattr(player2, 'action', mock_action_cheat)

    play_game(player1, player2)
    assert player1.score == -1
    assert player2.score == 3

def test_p1_cooperate_p2_cooperate(monkeypatch):
    player1, player2 = Player(), Player()

    monkeypatch.setattr(player1, 'action', mock_action_cooperate)
    monkeypatch.setattr(player2, 'action', mock_action_cooperate)

    play_game(player1, player2)
    assert player1.score == 2
    assert player2.score == 2


