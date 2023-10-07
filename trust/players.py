from trust.actions import TrustGameActions
import random
from abc import ABC, abstractmethod


class BasePlayer(ABC):
    @abstractmethod
    def action(self):
        ...


class RandomPlayer(BasePlayer):
    def action(self) -> TrustGameActions:
        return random.choice([i for i in TrustGameActions])


class AlwaysCooperatePlayer(BasePlayer):
    def action(self) -> TrustGameActions:
        return TrustGameActions.COOPERATE
    

class AlwaysCheatPlayer(BasePlayer):
    def action(self) -> TrustGameActions:
        return TrustGameActions.CHEAT