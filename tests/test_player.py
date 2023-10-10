from typing import List, Optional
import pytest
import random
from trust.players import BasePlayer, AlwaysCooperatePlayer, RandomPlayer, AlwaysCheatPlayer, CopycatPlayer, GrudgePlayer, DetectivePlayer
from trust.trust_game import TrustGameActions

class TestBasePlayer:
    class Player(BasePlayer):
        def action(self, opponent_history: List[TrustGameActions] | None = None):
            return self.update_and_return_action_history(TrustGameActions.CHEAT)
    
    def test_base_player_reset_history(self):
        player = self.Player()
        assert player.action() == TrustGameActions.CHEAT
        assert player.action() == TrustGameActions.CHEAT
        assert player._action_history == [TrustGameActions.CHEAT, TrustGameActions.CHEAT]

        player.reset_history()

        assert player._action_history == []

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
        player = CopycatPlayer()
        
        assert player.action([TrustGameActions.CHEAT]) == TrustGameActions.CHEAT
        assert player.action([TrustGameActions.COOPERATE]) == TrustGameActions.COOPERATE

    def test_player_action_empty_history(self):
        player = CopycatPlayer()

        assert player.action([]) == TrustGameActions.COOPERATE


class TestGrudgePlayer:
    def test_player_action(self):
        player = GrudgePlayer()
        
        assert player.action([TrustGameActions.COOPERATE]) == TrustGameActions.COOPERATE

    def test_player_action_once_cheated(self):
        player = GrudgePlayer()
        
        assert player.action([TrustGameActions.CHEAT, TrustGameActions.COOPERATE]) == TrustGameActions.CHEAT
    

class TestDetectivePlayer:
    start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
    # TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE
    
    def test_starting_action_sequence(self):
        player = DetectivePlayer()

        assert player.action([]) == TrustGameActions.COOPERATE
        assert player.action([]) == TrustGameActions.CHEAT
        assert player.action([]) == TrustGameActions.COOPERATE
        assert player.action([]) == TrustGameActions.COOPERATE

    def test_copycat_behaviour_after_starting_sequence(self):
        player = DetectivePlayer()
        
        player._action_history = self.start_sequence
        history = [TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
        assert player.action(history) == TrustGameActions.COOPERATE

        player._action_history = self.start_sequence
        history = [TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.CHEAT]
        assert player.action(history) == TrustGameActions.CHEAT

    def test_alwayscheat_behaviour_after_starting_sequence(self):
        player = DetectivePlayer()

        player._action_history = self.start_sequence
        history = [TrustGameActions.COOPERATE] * 4
        assert player.action(history) == TrustGameActions.CHEAT

    def test_switch_from_always_cheat_to_copycat(self):
        player = DetectivePlayer()

        player._action_history = self.start_sequence
        history = [TrustGameActions.COOPERATE] * 4
        assert player.action(history) == TrustGameActions.CHEAT

        history = history + [TrustGameActions.CHEAT]
        assert player.action(history) == TrustGameActions.CHEAT

        history  = history + [TrustGameActions.COOPERATE]
        assert player.action(history) == TrustGameActions.COOPERATE
    
