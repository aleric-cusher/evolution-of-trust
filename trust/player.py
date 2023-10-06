from trust.trust_game import TrustGameActions

class AlwaysCooperate:
    def __init__(self) -> None:
        self.score = 0
    
    def action(self):
        return TrustGameActions.COOPERATE