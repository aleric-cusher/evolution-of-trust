from trust.actions import TrustGameActions
import random
from abc import ABC, abstractmethod

class BasePlayer(ABC):
    def __init__(self) -> None:
        self.score = 0
    
    @abstractmethod
    def action(self):
        ...

class RandomPlayer(BasePlayer):
    def action(self) -> TrustGameActions:
        return random.choice([i for i in TrustGameActions])

class AlwaysCooperatePlayer(BasePlayer):
    def action(self) -> TrustGameActions:
        return TrustGameActions.COOPERATE
    
