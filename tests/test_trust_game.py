import pytest
import random
from trust.trust_game import TrustGame
from trust.actions import TrustGameActions
from trust.players import AlwaysCooperatePlayer, DetectivePlayer, RandomPlayer, AlwaysCheatPlayer, CopycatPlayer, GrudgePlayer


class TestTrustGame:
    def test_valid_run(self):
        try:
            game = TrustGame([AlwaysCooperatePlayer(), AlwaysCooperatePlayer()])
            game.play_game()
        except Exception as e:
            assert False, f'Exception {e}'
    
    def test_correct_attribute_initialization(self):
        player1_instance, player2_instance = RandomPlayer(), RandomPlayer()
        game = TrustGame([player1_instance, player2_instance])
        
        assert game.players[0] == player1_instance
        assert game.players[1] == player2_instance
        assert game.scorecard[player1_instance]['score'] == 0
        assert game.scorecard[player2_instance]['score'] == 0
        assert game.scorecard[player1_instance]['actions'] == []
        assert game.scorecard[player2_instance]['actions'] == []

    def test_invalid_player_types_in_trust_game(self):
        with pytest.raises(TypeError):
            TrustGame(['a', 4])

    def test_invalid_num_games_in_play_game(self):
        game = TrustGame([RandomPlayer(), RandomPlayer()])
        with pytest.raises(ValueError):
            game.play_game(0)

    def test_invalid_num_games_type_in_play_game(self):
        game = TrustGame([RandomPlayer(), RandomPlayer()])
        with pytest.raises(TypeError):
            game.play_game('a')

    def test_update_player_scores_method(self):
        player1_instance, player2_instance = RandomPlayer(), RandomPlayer()
        game = TrustGame([player1_instance, player2_instance])

        game.update_player_scores((400, 145), player1_instance, player2_instance)

        assert game.scorecard[player1_instance]['score'] == 400
        assert game.scorecard[player2_instance]['score'] == 145

    def test_update_player_actions(self):
        player1_instance, player2_instance = RandomPlayer(), RandomPlayer()
        game = TrustGame([player1_instance, player2_instance])

        game.update_player_actions((TrustGameActions.COOPERATE, TrustGameActions.CHEAT), player1_instance, player2_instance)
        game.update_player_actions((TrustGameActions.CHEAT, TrustGameActions.CHEAT), player1_instance, player2_instance)

        assert game.scorecard[player1_instance]['actions'] == [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]
        assert game.scorecard[player2_instance]['actions'] == [TrustGameActions.CHEAT, TrustGameActions.CHEAT]
    
    def test_get_scorecard_method(self):
        player1_instance, player2_instance, player3_instance = RandomPlayer(), RandomPlayer(), RandomPlayer()
        game = TrustGame((player1_instance, player2_instance, player3_instance))
        game.scorecard = {
            player1_instance: {'score': 3, 'actions': [TrustGameActions.CHEAT]},
            player2_instance: {'score': 2000, 'actions': []},
            player3_instance: {'score': 5, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]},
        }

        test_scorecard_1 = {
            player1_instance: {'score': 3, 'actions': [TrustGameActions.CHEAT]},
            player2_instance: {'score': 2000, 'actions': []}
        }

        test_scorecard_2 = {
            player2_instance: {'score': 2000, 'actions': []},
            player3_instance: {'score': 5, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]}
        }

        test_scorecard_3 = {
            player1_instance: {'score': 3, 'actions': [TrustGameActions.CHEAT]},
            player3_instance: {'score': 5, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]}
        }

        assert game._get_scorecard(player1_instance, player2_instance) == test_scorecard_1
        assert game._get_scorecard(player2_instance, player3_instance) == test_scorecard_2
        assert game._get_scorecard(player3_instance, player1_instance) == test_scorecard_3


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
        game = TrustGame([player1, player2])
        game.play_game()
        assert game.scorecard[player1]['score'] == player1_score
        assert game.scorecard[player2]['score'] == player2_score


class TestGamesBetweenSamePlayers:
    def test_always_cooperate_player_10_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCooperatePlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == 20
        assert game.scorecard[player2]['score'] == 20

    def test_always_cheat_player_10_games(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCheatPlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == 0
        assert game.scorecard[player2]['score'] == 0
    
    def test_copycat_player_10_games(self):
        player1, player2 = CopycatPlayer(), CopycatPlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == 20
        assert game.scorecard[player2]['score'] == 20
    
    def test_grudge_player_10_games(self):
        player1, player2 = GrudgePlayer(), GrudgePlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == 20
        assert game.scorecard[player2]['score'] == 20
    
    def test_detective_player_10_games(self):
        player1, player2 = DetectivePlayer(), DetectivePlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == 18
        assert game.scorecard[player2]['score'] == 18
    

class TestGamesBetweenDifferentPlayers:
    def mock_action_cheat(self, *args):
        return TrustGameActions.CHEAT
    
    def test_alwayscooperate_alwayscheat_10_games(self):
        player1, player2 = AlwaysCooperatePlayer(), AlwaysCheatPlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == -10
        assert game.scorecard[player2]['score'] == 30
    
    def test_alwayscooperate_alwayscheat_10_games_opposite(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        game = TrustGame([player1, player2])
        game.play_game(10)
        assert game.scorecard[player1]['score'] == 30
        assert game.scorecard[player2]['score'] == -10
    
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
        game = TrustGame([player1, player2])
        game.play_game(num_games)

        assert game.scorecard[player1]['score'] == player1_score
        assert game.scorecard[player2]['score'] == player2_score
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
        game = TrustGame([player1, player2])
        game.play_game(num_games)

        assert game.scorecard[player1]['score'] == player1_score
        assert game.scorecard[player2]['score'] == player2_score