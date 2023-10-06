import pytest
from trust.player import AlwaysCooperate
from trust.trust_game import TrustGameActions

def test_player_creation():
    player = AlwaysCooperate()
    assert player.score == 0

def test_player_alwayscooperate_action():
    player = AlwaysCooperate()
    assert player.action() == TrustGameActions.COOPERATE