import pytest
import random

from trust.actions import TrustGameActions
from trust.behaviours import (
    PlayerBehaviour,
    RandomBehaviour,
    AlwaysCheatBehaviour,
    AlwaysCooperateBehaviour,
    CopycatBehaviour,
    GrudgeBehaviour,
    DetectiveBehaviour
)

class TestRandomPlayer:
    def mock_random_choice(self, *args):
        return TrustGameActions.CHEAT

    def test_get_action(self, mocker):
        mocker.patch('random.choice', self.mock_random_choice)
        spy = mocker.spy(random, 'choice')

        assert RandomBehaviour.get_action() == TrustGameActions.CHEAT
        assert spy.call_count == 1


class TestAlwaysCooperatePlayer:
    def test_get_action(self):
        assert AlwaysCooperateBehaviour.get_action() == TrustGameActions.COOPERATE

    
class TestAlwaysCheatPlayer:
    def test_get_action(self):
        assert AlwaysCheatBehaviour.get_action() == TrustGameActions.CHEAT


class TestCopycatbehaviour:
    def test_missing_opponent_history(self):
        with pytest.raises(TypeError):
            assert CopycatBehaviour.get_action()

    def test_get_action(self):
        assert CopycatBehaviour.get_action([TrustGameActions.CHEAT]) == TrustGameActions.CHEAT
        assert CopycatBehaviour.get_action([TrustGameActions.COOPERATE]) == TrustGameActions.COOPERATE

    def test_get_action_empty_history(self):
        assert CopycatBehaviour.get_action([]) == TrustGameActions.COOPERATE


class TestGrudgePlayer:
    def test_missing_opponent_history(self):
        with pytest.raises(TypeError):
            assert GrudgeBehaviour.get_action()

    def test_get_action(self):
        assert GrudgeBehaviour.get_action([TrustGameActions.COOPERATE]) == TrustGameActions.COOPERATE

    def test_get_action_once_cheated(self):
        assert GrudgeBehaviour.get_action([TrustGameActions.CHEAT, TrustGameActions.COOPERATE]) == TrustGameActions.CHEAT
    

class TestDetectivePlayer:
    start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
    # TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE
    
    def test_missing_opponent_history(self):
        with pytest.raises(TypeError):
            assert DetectiveBehaviour.get_action()

    def test_starting_get_action_sequence(self):
        assert DetectiveBehaviour.get_action([], self.start_sequence[:0]) == TrustGameActions.COOPERATE
        assert DetectiveBehaviour.get_action([], self.start_sequence[:1]) == TrustGameActions.CHEAT
        assert DetectiveBehaviour.get_action([], self.start_sequence[:2]) == TrustGameActions.COOPERATE
        assert DetectiveBehaviour.get_action([], self.start_sequence[:3]) == TrustGameActions.COOPERATE

    def test_copycat_after_starting_sequence(self):
        history = [TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
        assert DetectiveBehaviour.get_action(history, self.start_sequence) == TrustGameActions.COOPERATE

        history = [TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.CHEAT]
        assert DetectiveBehaviour.get_action(history, self.start_sequence) == TrustGameActions.CHEAT

    def test_alwayscheat_after_starting_sequence(self):
        history = [TrustGameActions.COOPERATE] * 4
        assert DetectiveBehaviour.get_action(history, self.start_sequence) == TrustGameActions.CHEAT

    def test_switch_from_always_cheat_to_copycat(self):
        history = [TrustGameActions.COOPERATE] * 4
        assert DetectiveBehaviour.get_action(history, self.start_sequence) == TrustGameActions.CHEAT

        history = history + [TrustGameActions.CHEAT]
        assert DetectiveBehaviour.get_action(history, self.start_sequence) == TrustGameActions.CHEAT

        history  = history + [TrustGameActions.COOPERATE]
        assert DetectiveBehaviour.get_action(history, self.start_sequence) == TrustGameActions.COOPERATE