from __future__ import annotations
from typing import List, Optional, Any
from abc import ABC, abstractmethod

from trust.actions import TrustGameActions
import random
from copy import deepcopy


class BasePlayer(ABC):
    def __init__(self) -> None:
        super().__init__()
        self._action_history = []
    
    def update_and_return_action_history(self, action: TrustGameActions):
        self._action_history.append(action)
        return action
    
    @abstractmethod
    def action(self, opponent_history: Optional[List[TrustGameActions]] = None):
        ...

    def get_action_history(self):
        return deepcopy(self._action_history)


class RandomPlayer(BasePlayer):
    def action(self, opponent_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        return self.update_and_return_action_history(random.choice([i for i in TrustGameActions]))


class AlwaysCooperatePlayer(BasePlayer):
    def action(self, opponent_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        return self.update_and_return_action_history(TrustGameActions.COOPERATE)
    

class AlwaysCheatPlayer(BasePlayer):
    def action(self, opponent_history: Optional[List[TrustGameActions]] = None) -> TrustGameActions:
        return self.update_and_return_action_history(TrustGameActions.CHEAT)


class CopycatPlayer(BasePlayer):
    def action(self, opponent_history: List[TrustGameActions]) -> TrustGameActions:
        if len(opponent_history) < 1:
            return self.update_and_return_action_history(TrustGameActions.COOPERATE)
        return self.update_and_return_action_history(opponent_history[-1])

class GrudgePlayer(BasePlayer):
    def action(self, opponent_history: List[TrustGameActions]) -> TrustGameActions:
        if TrustGameActions.CHEAT in opponent_history:
            return self.update_and_return_action_history(TrustGameActions.CHEAT)
        return self.update_and_return_action_history(TrustGameActions.COOPERATE)

class DetectivePlayer(BasePlayer):
    start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
    def action(self, opponent_history: List[TrustGameActions]) -> TrustGameActions:
        if len(self._action_history) < 4:
            return self.update_and_return_action_history(self.start_sequence[len(self._action_history)])

        if TrustGameActions.CHEAT in opponent_history:
            return self.update_and_return_action_history(opponent_history[-1])

        return self.update_and_return_action_history(TrustGameActions.CHEAT)



        