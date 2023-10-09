import pytest
import random
from trust.players import AlwaysCooperatePlayer, RandomPlayer, AlwaysCheatPlayer, CopycatPlayer, GrudgePlayer, DetectivePlayer
from trust.trust_game import TrustGameActions


class TestRandomPlayer:
    def mock_random_choice(self, *args):
        return TrustGameActions.CHEAT

    def test_player_action(self, mocker):
        player = RandomPlayer()
        mocker.patch('random.choice', self.mock_random_choice)
        spy = mocker.spy(random, 'choice')

        assert player.action() == TrustGameActions.CHEAT
        assert spy.call_count == 1


class TestAlwaysCooperatePlayer:
    def test_player_action(self):
        player = AlwaysCooperatePlayer()
        assert player.action() == TrustGameActions.COOPERATE

    
class TestAlwaysCheatPlayer:
    def test_player_action(self):
        player = AlwaysCheatPlayer()
        assert player.action() == TrustGameActions.CHEAT


class TestCopycatplayer:
    def test_player_action(self):
        player1 = CopycatPlayer()
        player2 = CopycatPlayer()
        scorecard = {
            player1: {'score': 0, 'actions': [TrustGameActions.COOPERATE]},
            player2: {'score': 0, 'actions': [TrustGameActions.CHEAT]}
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT
        assert player2.action(scorecard) == TrustGameActions.COOPERATE

    def test_player_action_empty_scorecard(self):
        player1 = CopycatPlayer()
        player2 = CopycatPlayer()
        scorecard = {
            player1: {'score': 0, 'actions': []},
            player2: {'score': 0, 'actions': []}
        }
        assert player1.action(scorecard) == TrustGameActions.COOPERATE
        assert player2.action(scorecard) == TrustGameActions.COOPERATE

class TestGrudgePlayer:
    def test_player_action(self):
        player1 = GrudgePlayer()
        player2 = GrudgePlayer()
        scorecard = {
            player1: {'score': 0, 'actions': [TrustGameActions.COOPERATE]},
            player2: {'score': 0, 'actions': [TrustGameActions.COOPERATE]}
        }
        assert player1.action(scorecard) == TrustGameActions.COOPERATE
        assert player2.action(scorecard) == TrustGameActions.COOPERATE

    def test_player_action_once_cheated(self):
        player1 = GrudgePlayer()
        player2 = GrudgePlayer()
        scorecard = {
            player1: {'score': 0, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]},
            player2: {'score': 0, 'actions': [TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]}
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT
        assert player2.action(scorecard) == TrustGameActions.COOPERATE
    
class TestDetectivePlayer:
    def test_starting_action_sequence(self):
        # TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE
        player1 = DetectivePlayer()
        player2 = DetectivePlayer()
        scorecard = {
            player1: {'score': 0, 'actions': []},
            player2: {'score': 0, 'actions': []}
        }
        assert player1.action(scorecard) == TrustGameActions.COOPERATE

        scorecard = {**scorecard, player1: {'actions': [TrustGameActions.COOPERATE]}}
        assert player1.action(scorecard) == TrustGameActions.CHEAT

        scorecard = {**scorecard, player1: {'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]}}
        assert player1.action(scorecard) == TrustGameActions.COOPERATE

        scorecard = {**scorecard, player1: {'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE]}}
        assert player1.action(scorecard) == TrustGameActions.COOPERATE

    def test_copycat_behaviour_after_starting_sequence(self):
        start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
        player1 = DetectivePlayer()
        player2 = DetectivePlayer()
        scorecard = {
            player1: {'score': 0, 'actions': start_sequence + [TrustGameActions.COOPERATE]},
            player2: {'score': 0, 'actions': start_sequence + [TrustGameActions.CHEAT]}
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT

        scorecard = {
            player1: {'score': 0, 'actions': start_sequence + [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]},
            player2: {'score': 0, 'actions': start_sequence + [TrustGameActions.CHEAT, TrustGameActions.COOPERATE]}
        }
        assert player1.action(scorecard) == TrustGameActions.COOPERATE

    def test_alwayscheat_behaviour_after_starting_sequence(self):
        start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
        player1 = DetectivePlayer()
        player2 = DetectivePlayer()
        scorecard = {
            player1: {'score': 0, 'actions': start_sequence},
            player2: {'score': 0, 'actions': [TrustGameActions.COOPERATE] * 4}
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT

        scorecard = {
            player1: {'score': 0, 'actions': start_sequence + [TrustGameActions.CHEAT]},
            player2: {'score': 0, 'actions': [TrustGameActions.COOPERATE] * 5}
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT

    def test_switch_from_always_cheat_to_copycat(self):
        start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
        player1 = DetectivePlayer()
        player2 = DetectivePlayer()
        scorecard = {
            player1: {'score': 0, 'actions': start_sequence},
            player2: {'score': 0, 'actions': [TrustGameActions.COOPERATE] * 4}
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT

        scorecard = {
            player1: {'score': 0, 'actions': start_sequence + [TrustGameActions.CHEAT]},
            player2: {'score': 0, 'actions': ([TrustGameActions.COOPERATE] * 4) + [TrustGameActions.CHEAT] }
        }
        assert player1.action(scorecard) == TrustGameActions.CHEAT

        scorecard = {
            player1: {'score': 0, 'actions': start_sequence + [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 0, 'actions': ([TrustGameActions.COOPERATE] * 4) + [TrustGameActions.CHEAT, TrustGameActions.COOPERATE] }
        }
        assert player1.action(scorecard) == TrustGameActions.COOPERATE
    
