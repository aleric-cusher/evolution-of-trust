from enum import Enum, auto

class TrustGameActions(Enum):
    CHEAT = auto()
    COOPERATE = auto()

outcomes = {
    (TrustGameActions.CHEAT, TrustGameActions.CHEAT): (0, 0),
    (TrustGameActions.CHEAT, TrustGameActions.COOPERATE): (3, -1),
    (TrustGameActions.COOPERATE, TrustGameActions.CHEAT): (-1, 3),
    (TrustGameActions.COOPERATE, TrustGameActions.COOPERATE): (2, 2),    
}

def play_game(player1_choice, player2_choice):
    return outcomes[(player1_choice, player2_choice)]
    