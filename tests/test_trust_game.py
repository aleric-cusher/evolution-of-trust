import pytest
import random
from trust.trust_game import TrustGame
from trust.actions import TrustGameActions
from trust.players import AlwaysCooperatePlayer, DetectivePlayer, RandomPlayer, AlwaysCheatPlayer, CopycatPlayer, GrudgePlayer


class TestTrustGame:
    def test_valid_run(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        try:
            game = TrustGame(player1, player2)
            game.play_game()
        except Exception as e:
            assert False, f'Exception {e}'
    
    def test_correct_attribute_initialization(self):
        player1, player2 = RandomPlayer(), RandomPlayer()
        game = TrustGame(player1, player2)
        
        assert game.player1 == player1
        assert game.player2 == player2

    def test_invalid_player_types_in_trust_game(self):
        with pytest.raises(TypeError):
            TrustGame('a', 4)

    def test_invalid_num_games_in_play_game(self):
        game = TrustGame(RandomPlayer(), RandomPlayer())
        with pytest.raises(ValueError):
            game.play_game(0)

    def test_invalid_num_games_type_in_play_game(self):
        player1, player2 = RandomPlayer(), RandomPlayer()
        game = TrustGame(player1, player2)
        with pytest.raises(TypeError):
            game.play_game('a')


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
        game = TrustGame(player1, player2)
        score_handler = game.play_game()
        scorecard = score_handler.get_scorecard()

        assert game.scorecard.get_score(player1) == player1_score
        assert game.scorecard.get_score(player2) == player2_score


class TestGamesBetweenSamePlayers:
    def test_always_cooperate_player_tournament(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        game = TrustGame(player1, player2)
        game.play_game(10)
        scorecard = game.scorecard.get_scorecard()

        assert game.scorecard.get_score(player1) == 20
        assert game.scorecard.get_score(player2) == 20

    def test_always_cheat_player_tournament(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCheatPlayer()
        game = TrustGame(player1, player2)
        game.play_game(10)
        scorecard = game.scorecard.get_scorecard()

        assert game.scorecard.get_score(player1) == 0
        assert game.scorecard.get_score(player2) == 0
    
    def test_copycat_player_tournament(self):
        player1, player2 = CopycatPlayer(), CopycatPlayer()
        game = TrustGame(player1, player2)
        game.play_game(10)

        assert game.scorecard.get_score(player1) == 20
        assert game.scorecard.get_score(player2) == 20
    
    def test_grudge_player_tournament(self):
        player1, player2 = GrudgePlayer(), GrudgePlayer()
        game = TrustGame(player1, player2)
        game.play_game(10)

        assert game.scorecard.get_score(player1) == 20
        assert game.scorecard.get_score(player2) == 20
    
    def test_detective_player_tournament(self):
        player1, player2 = DetectivePlayer(), DetectivePlayer()
        game = TrustGame(player1, player2)
        game.play_game(10)

        assert game.scorecard.get_score(player1) == 18
        assert game.scorecard.get_score(player2) == 18
    

class TestGamesBetweenDifferentPlayers:
    def mock_action_cheat(self, *args):
        return TrustGameActions.CHEAT
    
    def test_alwayscooperate_alwayscheat_tournament(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCheatPlayer()
        game = TrustGame(player1, player2)
        game.play_game(10)

        assert game.scorecard.get_score(player1) == -10
        assert game.scorecard.get_score(player2) == 30
    
    with_random_player_parameters = [
        # (player1_class, player2_class, num_games, player1_score, player2_score)
        (RandomPlayer, AlwaysCheatPlayer, 10, 0, 0),
        (RandomPlayer, AlwaysCooperatePlayer, 10, 30, -10),
    ]

    @pytest.mark.parametrize('player1_class, player2_class, num_games, player1_score, player2_score', with_random_player_parameters)
    def test_games_between_different_players_with_randomplayer(self, mocker, player1_class, player2_class, num_games, player1_score, player2_score):
        mocker.patch('random.choice', self.mock_action_cheat)
        spy = mocker.spy(random, 'choice')

        player1, player2 = player1_class(), player2_class()
        game = TrustGame(player1, player2)
        game.play_game(num_games)

        assert game.scorecard.get_score(player1) == player1_score
        assert game.scorecard.get_score(player2) == player2_score
        assert spy.call_count == num_games
    
    without_random_player_parameters = [
        # (player1_class, player2_class, num_games, player1_score, player2_score)
        (CopycatPlayer, AlwaysCooperatePlayer, 10, 20, 20),
        (CopycatPlayer, AlwaysCheatPlayer, 10, -1, 3),
        (GrudgePlayer, AlwaysCheatPlayer, 10, -1, 3),        
        (GrudgePlayer, AlwaysCooperatePlayer, 10, 20, 20),
        (GrudgePlayer, CopycatPlayer, 10, 20, 20),
        (DetectivePlayer, CopycatPlayer, 10, 18, 18),
        (DetectivePlayer, AlwaysCheatPlayer, 10, -3, 9),
        (DetectivePlayer, AlwaysCooperatePlayer, 10, 27, -1),
        (DetectivePlayer, GrudgePlayer, 10, 3, 7),
    ]

    @pytest.mark.parametrize('player1_class, player2_class, num_games, player1_score, player2_score', without_random_player_parameters)
    def test_games_between_different_players_without_randomplayer(self, player1_class, player2_class, num_games, player1_score, player2_score):
        player1, player2 = player1_class(), player2_class()
        game = TrustGame(player1, player2)
        game.play_game(num_games)
        
        assert game.scorecard.get_score(player1) == player1_score
        assert game.scorecard.get_score(player2) == player2_score

