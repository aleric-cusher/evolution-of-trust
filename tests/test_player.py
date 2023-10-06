import pytest
import random
from trust.players import AlwaysCooperatePlayer, RandomPlayer, AlwaysCheatPlayer
from trust.trust_game import TrustGameActions


class TestRandomPlayer:
    def mock_random_choice(self, *args):
        return TrustGameActions.CHEAT
    
    def test_creation(self):
        player = RandomPlayer()
        assert player.score == 0

    def test_player_action(self, mocker):
        player = RandomPlayer()
        mocker.patch('random.choice', self.mock_random_choice)
        spy = mocker.spy(random, 'choice')

        assert player.action() == TrustGameActions.CHEAT
        assert spy.call_count == 1


class TestAlwaysCooperatePlayer:
    def test_creation(self):
        player = AlwaysCooperatePlayer()
        assert player.score == 0

    def test_player_action(self):
        player = AlwaysCooperatePlayer()
        assert player.action() == TrustGameActions.COOPERATE

    
class TestAlwaysCheatPlayer:
    def test_creation(self):
        player = AlwaysCheatPlayer()
        assert player.score == 0

    def test_player_action(self):
        player = AlwaysCheatPlayer()
        assert player.action() == TrustGameActions.CHEAT