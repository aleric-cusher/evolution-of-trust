import pytest
import random
from trust.players import AlwaysCooperatePlayer, RandomPlayer, AlwaysCheatPlayer, CopycatPlayer
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

