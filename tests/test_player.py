import pytest
import random
from trust.players import AlwaysCooperatePlayer, RandomPlayer
from trust.trust_game import TrustGameActions

class TestRandomPlayer:
    def test_creation(self):
        player = RandomPlayer()
        assert player.score == 0

    def test_player_action(self):
        player = RandomPlayer()
        random.seed(0)
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.CHEAT

class TestAlwaysCooperatePlayer:
    def test_creation(self):
        player = AlwaysCooperatePlayer()
        assert player.score == 0

    def test_player_action(self):
        player = AlwaysCooperatePlayer()
        assert player.action() == TrustGameActions.COOPERATE