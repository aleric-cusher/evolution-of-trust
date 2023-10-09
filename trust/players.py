from __future__ import annotations
from trust.actions import TrustGameActions
from typing import Optional, Any
import random
from abc import ABC, abstractmethod


class BasePlayer(ABC):
    @abstractmethod
    def action(self, scorecard:Optional[dict[BasePlayer, dict[str, Any]]] = None):
        ...


class RandomPlayer(BasePlayer):
    def action(self, scorecard:Optional[dict[BasePlayer, dict[str, Any]]] = None) -> TrustGameActions:
        return random.choice([i for i in TrustGameActions])


class AlwaysCooperatePlayer(BasePlayer):
    def action(self, scorecard:Optional[dict[BasePlayer, dict[str, Any]]] = None) -> TrustGameActions:
        return TrustGameActions.COOPERATE
    

class AlwaysCheatPlayer(BasePlayer):
    def action(self, scorecard:Optional[dict[BasePlayer, dict[str, Any]]] = None) -> TrustGameActions:
        return TrustGameActions.CHEAT


class CopycatPlayer(BasePlayer):
    def action(self, scorecard:dict[BasePlayer, dict[str, Any]]) -> TrustGameActions:
        other_player = [player for player in scorecard.keys() if player != self][0]
        other_player_actions = scorecard[other_player]['actions']
        if len(other_player_actions) < 1:
            return TrustGameActions.COOPERATE
        return other_player_actions[-1]

class GrudgePlayer(BasePlayer):
    def action(self, scorecard: dict[BasePlayer, dict[str, Any]]) -> TrustGameActions:
        other_player = [player for player in scorecard.keys() if player != self][0]
        other_player_actions = scorecard[other_player]['actions']
        if TrustGameActions.CHEAT in other_player_actions:
            return TrustGameActions.CHEAT
        return TrustGameActions.COOPERATE

class DetectivePlayer(BasePlayer):
    start_sequence = [TrustGameActions.COOPERATE, TrustGameActions.CHEAT, TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
    def action(self, scorecard: dict[BasePlayer, dict[str, Any]]) -> TrustGameActions:
        self_actions = scorecard[self]['actions']

        if len(self_actions) < 4:
            return self.start_sequence[len(self_actions)]
        
        other_player = [player for player in scorecard.keys() if player != self][0]
        other_player_actions = scorecard[other_player]['actions']

        if TrustGameActions.CHEAT in other_player_actions:
            return other_player_actions[-1]
        
        return TrustGameActions.CHEAT



        