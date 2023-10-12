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
        with pytest.raises(RuntimeError):
            player.action()
        
        player.new_game(player)
        assert player.action() == TrustGameActions.COOPERATE
        assert player.action() == TrustGameActions.COOPERATE
        assert player.get_action_history() == [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]


    def test_get_action_history(self):
        player = BasePlayer(AlwaysCooperatePlayer)
        player._action_history = [TrustGameActions.CHEAT, TrustGameActions.CHEAT]
        assert player.get_action_history() == [TrustGameActions.CHEAT, TrustGameActions.CHEAT]

    def test_new_game(self):
        player1 = AlwaysCheatPlayer()
        player2 = AlwaysCooperatePlayer()

        player1._action_history = [TrustGameActions.CHEAT, TrustGameActions.COOPERATE]

        player1.new_game(player2)
        assert player1.opponent == player2
        assert player1._action_history == []

        player2.new_game(player1)
        assert player2.opponent == player1
        
    def test_new_game_invalid_opponent(self):
        player1 = AlwaysCheatPlayer()
        
        with pytest.raises(TypeError):
            player1.new_game('player2')

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
    
