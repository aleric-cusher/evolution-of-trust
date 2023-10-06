from trust.trust_game import TrustGameActions
import random

class Player:
    def __init__(self) -> None:
        self.score = 0

    def action(self) -> TrustGameActions:
        return random.choice([i for i in TrustGameActions])

class AlwaysCooperate:
    def __init__(self) -> None:
        self.score = 0
    
    def action(self) -> TrustGameActions:
        return TrustGameActions.COOPERATE