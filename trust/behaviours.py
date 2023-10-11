from abc import ABC, abstractstaticmethod
from typing import List, Optional
import random

from trust.actions import TrustGameActions


class PlayerBehaviour(ABC):
    @abstractstaticmethod
    def get_action(opponent_history: Optional[List[TrustGameActions]] = None, self_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        pass


class AlwaysCheatBehaviour(PlayerBehaviour):
    def get_action(opponent_history: Optional[List[TrustGameActions]] = None, self_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        return TrustGameActions.CHEAT


class AlwaysCooperateBehaviour(PlayerBehaviour):
    def get_action(opponent_history: Optional[List[TrustGameActions]] = None, self_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        return TrustGameActions.COOPERATE


class RandomBehaviour(PlayerBehaviour):
    def get_action(opponent_history: Optional[List[TrustGameActions]] = None, self_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        return random.choice(list(TrustGameActions))


class CopycatBehaviour(PlayerBehaviour):
    def get_action(opponent_history: List[TrustGameActions], self_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        if len(opponent_history) < 1:
            return TrustGameActions.COOPERATE
        return opponent_history[-1]


class GrudgeBehaviour(PlayerBehaviour):
    def get_action(opponent_history: List[TrustGameActions], self_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        if TrustGameActions.CHEAT in opponent_history:
            return TrustGameActions.CHEAT
        return TrustGameActions.COOPERATE


class DetectiveBehaviour(PlayerBehaviour):
    start_sequence: List[TrustGameActions] = [
        TrustGameActions.COOPERATE,
        TrustGameActions.CHEAT,
        TrustGameActions.COOPERATE,
        TrustGameActions.COOPERATE
    ]

    def get_action(opponent_history: List[TrustGameActions], self_history: List[TrustGameActions]) -> TrustGameActions:
        if len(self_history) < 4:
            return DetectiveBehaviour.start_sequence[len(self_history)]

        if TrustGameActions.CHEAT in opponent_history:
            return opponent_history[-1]

        return TrustGameActions.CHEAT
