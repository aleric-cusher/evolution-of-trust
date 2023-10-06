import pytest
from trust.actions import TrustGameActions

def test_cheat_enum():
    assert TrustGameActions.CHEAT in TrustGameActions

def test_cooperate_enum():
    assert TrustGameActions.COOPERATE in TrustGameActions