from trust.player import BasePlayer
from trust.actions import TrustGameActions

outcomes = {
    (TrustGameActions.CHEAT, TrustGameActions.CHEAT): (0, 0),
    (TrustGameActions.CHEAT, TrustGameActions.COOPERATE): (3, -1),
    (TrustGameActions.COOPERATE, TrustGameActions.CHEAT): (-1, 3),
    (TrustGameActions.COOPERATE, TrustGameActions.COOPERATE): (2, 2),    
}

def play_game(player1, player2):
    if not (isinstance(player1, BasePlayer) and isinstance(player2, BasePlayer)):
        raise TypeError('Invalid player actions')
    player1_outcome, player2_outcome =  outcomes[(player1.action(), player2.action())]
    player1.score += player1_outcome
    player2.score += player2_outcome
    