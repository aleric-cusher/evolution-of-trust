import pytest
import random
from trust.trust_game import play_game
from trust.actions import TrustGameActions
from trust.players import AlwaysCooperatePlayer, RandomPlayer, AlwaysCheatPlayer


class TestPlayGame:
    def test_invalid_player_types_in_play_game(self):
        with pytest.raises(TypeError):
            play_game('a', 4)

    def test_invalid_num_games_in_play_game(self):
        with pytest.raises(ValueError):
            play_game(RandomPlayer(), RandomPlayer(), 0)

    def test_invalid_num_games_in_play_game(self):
        with pytest.raises(TypeError):
            play_game(RandomPlayer(), RandomPlayer(), 'a')
    
    def test_valid_run(self):
        try:
            play_game(AlwaysCooperatePlayer(), AlwaysCooperatePlayer())
        except Exception as e:
            assert False, f'Exception {e}'


class TestAllActionCombinations:
    combination_parameters = [
        # (player1_class, player2_class, player1_score, player2_score)
        (AlwaysCheatPlayer, AlwaysCheatPlayer, 0, 0),
        (AlwaysCheatPlayer, AlwaysCooperatePlayer, 3, -1),
        (AlwaysCooperatePlayer, AlwaysCheatPlayer, -1, 3),
        (AlwaysCooperatePlayer, AlwaysCooperatePlayer, 2, 2)
    ]

    @pytest.mark.parametrize('player1_class, player2_class, player1_score, player2_score', combination_parameters)
    def test_action_combinations(self, player1_class, player2_class, player1_score, player2_score):
        player1, player2 = player1_class(), player2_class()
        play_game(player1, player2)
        assert player1.score == player1_score
        assert player2.score == player2_score


class TestGamesBetweenSamePlayers:
    def test_always_cooperate_player_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2)
        assert player1.score == 2
        assert player2.score == 2

    def test_always_cooperate_player_5_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2, num_games=5)
        assert player1.score == 10
        assert player2.score == 10

    def test_always_cooperate_player_10_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2, num_games=10)
        assert player1.score == 20
        assert player2.score == 20

    def test_always_cheat_player_games(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCheatPlayer()
        play_game(player1, player2)
        assert player1.score == 0
        assert player2.score == 0

    def test_always_cheat_player_5_games(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCheatPlayer()
        play_game(player1, player2, num_games=5)
        assert player1.score == 0
        assert player2.score == 0

    def test_always_cheat_player_10_games(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCheatPlayer()
        play_game(player1, player2, num_games=10)
        assert player1.score == 0
        assert player2.score == 0
    

class TestGamesBetweenDifferentPlayers:
    def mock_action_cheat(self, *args):
        return TrustGameActions.CHEAT
    
    def test_alwayscooperate_alwayscheat_10_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCheatPlayer()
        play_game(player1, player2, num_games=10)
        assert player1.score == -10
        assert player2.score == 30
    
    def test_alwayscooperate_alwayscheat_10_games_opposite(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        play_game(player1, player2, num_games=10)
        assert player1.score == 30
        assert player2.score == -10
    
    parameters = [
        # (player1_class, player2_class, num_games, player1_score, player2_score)
        (RandomPlayer, AlwaysCheatPlayer, 10, 0, 0),
        (RandomPlayer, AlwaysCooperatePlayer, 10, 30, -10),
    ]

    @pytest.mark.parametrize('player1_class, player2_class, num_games, player1_score, player2_score', parameters)
    def test_games_between_different_players(self, mocker, player1_class, player2_class, num_games, player1_score, player2_score):
        mocker.patch('random.choice', self.mock_action_cheat)
        spy = mocker.spy(random, 'choice')

        player1, player2 = player1_class(), player2_class()
        play_game(player1, player2, num_games=num_games)

        assert player1.score == player1_score
        assert player2.score == player2_score
        assert spy.call_count == num_games