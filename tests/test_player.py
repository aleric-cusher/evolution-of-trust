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
    def test_action(self, mocker):
        player = BasePlayer(AlwaysCooperateBehaviour)

        class MockGame:
            def get_opponent(self, player):
                return player

        class MockScorecard:
            def get_actions(self, player):
                return [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]

            def update_actions(self, action, scorecard):
                pass
        
        game = MockGame()
        scorecard = MockScorecard()

        # spy_get_opponent = mocker.spy(game, 'get_opponent')
        # spy_get_actions = mocker.spy(scorecard, 'get_actions')
        # spy_update_actions = mocker.spy(scorecard, 'update_actions')
        player.action(game, scorecard)
        # assert player.action(game, scorecard) == TrustGameActions.COOPERATE
        # assert player.action(game, scorecard) == TrustGameActions.COOPERATE
        # assert spy_get_opponent.call_count == 2
        # assert spy_get_actions.call_count == 2
        # assert spy_update_actions.call_count == 2


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
    
