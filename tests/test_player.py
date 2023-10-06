import pytest
import random
from trust.player import AlwaysCooperate, Player
from trust.trust_game import TrustGameActions

class TestPlayer:
    def test_creation(self):
        player = Player()
        assert player.score == 0

    def test_player_action(self):
        player = Player()
        random.seed(0)
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.CHEAT

class TestAlwaysCooperate:
    def test_creation(self):
        player = AlwaysCooperate()
        assert player.score == 0

    def test_player_action(self):
        player = AlwaysCooperate()
        assert player.action() == TrustGameActions.COOPERATE