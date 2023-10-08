from __future__ import annotations
from trust.actions import TrustGameActions
from typing import Optional
import random
from abc import ABC, abstractmethod


class BasePlayer(ABC):
    @abstractmethod
    def action(self, scorecard:dict[BasePlayer, dict[str, any]] = None):
        ...


class RandomPlayer(BasePlayer):
    def action(self, scorecard:dict[BasePlayer, dict[str, any]] = None) -> TrustGameActions:
        return random.choice([i for i in TrustGameActions])


class AlwaysCooperatePlayer(BasePlayer):
    def action(self, scorecard:dict[BasePlayer, dict[str, any]] = None) -> TrustGameActions:
        return TrustGameActions.COOPERATE
    

class AlwaysCheatPlayer(BasePlayer):
    def action(self, scorecard:dict[BasePlayer, dict[str, any]] = None) -> TrustGameActions:
        return TrustGameActions.CHEAT


class CopycatPlayer(BasePlayer):
    def action(self, scorecard:dict[BasePlayer, dict[str, any]]):
        other_player = [player for player in scorecard.keys() if player != self][0]
        other_player_actions = scorecard[other_player]['actions']
        if len(other_player_actions) < 1:
            return TrustGameActions.COOPERATE
        return other_player_actions[-1]
        