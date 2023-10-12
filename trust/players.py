from __future__ import annotations
from typing import List, Optional

from trust.behaviours import (
    PlayerBehaviour,
    RandomBehaviour,
    AlwaysCheatBehaviour,
    AlwaysCooperateBehaviour,
    CopycatBehaviour,
    GrudgeBehaviour,
    DetectiveBehaviour
)

from trust.actions import TrustGameActions
from copy import deepcopy


class BasePlayer:
    def __init__(self, behaviour: PlayerBehaviour) -> None:
        super().__init__()
        self._action_history = []
        self.behaviour = behaviour
        self.opponent: BasePlayer = None
    
    def _update_and_return_action_history(self, action: TrustGameActions) -> TrustGameActions:
        self._action_history.append(action)
        return action

    def get_action_history(self) -> List[TrustGameActions]:
        return deepcopy(self._action_history)
    
    def action(self) -> TrustGameActions:
        if self.behaviour is None:
            raise Exception('Please define a behaviour')
        
        if self.opponent is None:
            raise RuntimeError('Please run the new_game method before calling action.')
        
        opponent_history = self.opponent.get_action_history()
        self_history = self.get_action_history()
        min_index = min([len(opponent_history), len(self_history)])
        action = self.behaviour.get_action(opponent_history[: min_index], self_history[: min_index])
        return self._update_and_return_action_history(action)
    
    def new_game(self, opponent: BasePlayer) -> None:
        if not isinstance(opponent, BasePlayer):
            raise TypeError('Parameter: opponent should be of the type BasePlayer')
        
        self._action_history = []
        self.opponent = opponent
    


class RandomPlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__(RandomBehaviour)


class AlwaysCooperatePlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__(AlwaysCooperateBehaviour)
    

class AlwaysCheatPlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__(AlwaysCheatBehaviour)


class CopycatPlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__(CopycatBehaviour)


class GrudgePlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__(GrudgeBehaviour)   


class DetectivePlayer(BasePlayer):
    def __init__(self) -> None:
        super().__init__(DetectiveBehaviour) 
