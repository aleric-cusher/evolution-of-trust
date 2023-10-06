import pytest
from trust.trust_game import play_game
from trust.actions import TrustGameActions
from trust.players import AlwaysCooperatePlayer, RandomPlayer

def mock_action_cheat():
    return TrustGameActions.CHEAT

def mock_action_cooperate():
    return TrustGameActions.COOPERATE

def test_invalid_player_types_in_play_game():
    with pytest.raises(TypeError):
        play_game('a', 4)

def test_invalid_num_games_in_play_game():
    with pytest.raises(ValueError):
        play_game(RandomPlayer(), RandomPlayer(), 0)

def test_invalid_num_games_in_play_game():
    with pytest.raises(TypeError):
        play_game(RandomPlayer(), RandomPlayer(), 'a')

def test_p1_cheat_p2_cheat(monkeypatch):
    player1, player2 = RandomPlayer(), RandomPlayer()

    monkeypatch.setattr(player1, 'action', mock_action_cheat)
    monkeypatch.setattr(player2, 'action', mock_action_cheat)

    play_game(player1, player2)
    assert player1.score == 0
    assert player2.score == 0

def test_p1_cheat_p2_cooperate(monkeypatch):
    player1, player2 = RandomPlayer(), RandomPlayer()

    monkeypatch.setattr(player1, 'action', mock_action_cheat)
    monkeypatch.setattr(player2, 'action', mock_action_cooperate)

    play_game(player1, player2)
    assert player1.score == 3
    assert player2.score == -1

def test_p1_cooperate_p2_cheat(monkeypatch):
    player1, player2 = RandomPlayer(), RandomPlayer()

    monkeypatch.setattr(player1, 'action', mock_action_cooperate)
    monkeypatch.setattr(player2, 'action', mock_action_cheat)

    play_game(player1, player2)
    assert player1.score == -1
    assert player2.score == 3

def test_p1_cooperate_p2_cooperate(monkeypatch):
    player1, player2 = RandomPlayer(), RandomPlayer()

    monkeypatch.setattr(player1, 'action', mock_action_cooperate)
    monkeypatch.setattr(player2, 'action', mock_action_cooperate)

    play_game(player1, player2)
    assert player1.score == 2
    assert player2.score == 2

def test_always_cooperate_player_games():
    player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
    play_game(player1, player2)
    assert player1.score == 2
    assert player2.score == 2

def test_always_cooperate_player_10_games():
    player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
    play_game(player1, player2, num_games=5)
    assert player1.score == 10
    assert player2.score == 10

def test_always_cooperate_player_10_games():
    player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
    play_game(player1, player2, num_games=10)
    assert player1.score == 20
    assert player2.score == 20
