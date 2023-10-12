from typing import List, Optional
import pytest
import random
from trust.players import BasePlayer, AlwaysCooperatePlayer, PlayerBehaviour, RandomPlayer, AlwaysCheatPlayer, CopycatPlayer, GrudgePlayer, DetectivePlayer
from trust.behaviours import (
    PlayerBehaviour,
    RandomBehaviour,
    AlwaysCheatBehaviour,
    AlwaysCooperateBehaviour,
    CopycatBehaviour,
    GrudgeBehaviour,
    DetectiveBehaviour
)
from trust.trust_game import TrustGameActions

class TestBasePlayer:
    def test_action(self):
        player = BasePlayer(AlwaysCooperateBehaviour)
        assert player.action(player) == TrustGameActions.COOPERATE
        assert player.action(player) == TrustGameActions.COOPERATE
        assert player.get_action_history() == [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]


    def test_get_action_history_and_reset_history(self):
        player = BasePlayer(AlwaysCooperatePlayer)
        player._action_history = [TrustGameActions.CHEAT, TrustGameActions.CHEAT]
        assert player.get_action_history() == [TrustGameActions.CHEAT, TrustGameActions.CHEAT]

        player.reset_history()
        assert player._action_history == []

class TestRandomPlayer:
    def test_player_attributes(self):
        player = RandomPlayer()
        assert player.behaviour == RandomBehaviour


class TestAlwaysCooperatePlayer:
    def test_player_attributes(self):
        player = AlwaysCooperatePlayer()
        assert player.behaviour == AlwaysCooperateBehaviour

    
class TestAlwaysCheatPlayer:
    def test_player_attributes(self):
        player = AlwaysCheatPlayer()
        assert player.behaviour == AlwaysCheatBehaviour


class TestCopycatplayer:
    def test_player_attributes(self):
        player = CopycatPlayer()
        assert player.behaviour == CopycatBehaviour


class TestGrudgePlayer:
    def test_player_attributes(self):
        player = GrudgePlayer()
        assert player.behaviour == GrudgeBehaviour


class TestDetectivePlayer:
    def test_player_attributes(self):
        player = DetectivePlayer()
        assert player.behaviour == DetectiveBehaviour
    
