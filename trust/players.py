from __future__ import annotations
from typing import List, Optional, TYPE_CHECKING, Type
from copy import deepcopy

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
if TYPE_CHECKING:
    from trust.scorecard import Scorecard
    from trust.trust_game import TrustGame



class BasePlayer:
    def __init__(self, behaviour: Type[PlayerBehaviour]) -> None:
        super().__init__()
        self.behaviour = behaviour
    
    def _update_and_return_action(self, action: TrustGameActions, scorecard: Scorecard) -> TrustGameActions:
        scorecard.update_actions(action, self)
        return action
    
    def action(self, game: TrustGame, scorecard: Scorecard) -> TrustGameActions:
        if self.behaviour is None:
            raise Exception('Please define a behaviour')
        
        opponent = game.get_opponent(self)
        opponent_history = scorecard.get_actions(opponent)
        self_history = scorecard.get_actions(self)
        action = self.behaviour.get_action(opponent_history[: len(self_history)], self_history)
        return self._update_and_return_action(action, scorecard)


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
