import pytest
import random
from trust.players import AlwaysCooperatePlayer, RandomPlayer, AlwaysCheatPlayer
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
        assert player.action() == TrustGameActions.COOPERATE


class TestAlwaysCooperatePlayer:
    def test_creation(self):
        player = AlwaysCooperatePlayer()
        assert player.score == 0

    def test_player_action(self):
        player = AlwaysCooperatePlayer()
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.COOPERATE

    
class TestAlwaysCheatPlayer:
    def test_creation(self):
        player = AlwaysCheatPlayer()
        assert player.score == 0

    def test_player_action(self):
        player = AlwaysCheatPlayer()
        assert player.action() == TrustGameActions.CHEAT
        assert player.action() == TrustGameActions.CHEAT
        assert player.action() == TrustGameActions.CHEAT
        assert player.action() == TrustGameActions.CHEAT