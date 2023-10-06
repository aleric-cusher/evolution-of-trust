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


class TestAllActionCombinations:
    all_possible_combination_parameters = [
        # (player1_action_func, player2_action_func, player1_score, player2_score)
        (mock_action_cheat, mock_action_cheat, 0, 0),
        (mock_action_cheat, mock_action_cooperate, 3, -1),
        (mock_action_cooperate, mock_action_cheat, -1, 3),
        (mock_action_cooperate, mock_action_cooperate, 2, 2)
    ]

    @pytest.mark.parametrize('player1_action_func, player2_action_func, player1_score, player2_score', all_possible_combination_parameters)
    def test_all_action_combinations(self, monkeypatch, player1_action_func, player2_action_func, player1_score, player2_score):
        player1, player2 = RandomPlayer(), RandomPlayer()

        monkeypatch.setattr(player1, 'action', player1_action_func)
        monkeypatch.setattr(player2, 'action', player2_action_func)

        play_game(player1, player2)
        assert player1.score == player1_score
        assert player2.score == player2_score

class TestGamesBetweenTwoPlayers:
    def test_always_cooperate_player_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2)
        assert player1.score == 2
        assert player2.score == 2

    def test_always_cooperate_player_10_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2, num_games=5)
        assert player1.score == 10
        assert player2.score == 10

    def test_always_cooperate_player_10_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2, num_games=10)
        assert player1.score == 20
        assert player2.score == 20
