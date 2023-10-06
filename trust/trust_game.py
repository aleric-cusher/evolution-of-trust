from enum import Enum, auto

class TrustGameActions(Enum):
    CHEAT = auto()
    COOPERATE = auto()


def play_game(player1_choice, player2_choice):
    if player1_choice == TrustGameActions.CHEAT and player2_choice == TrustGameActions.CHEAT:
        player1_outcome = 0
        player2_outcome = 0
        return player1_outcome, player2_outcome
    elif player1_choice == TrustGameActions.CHEAT and player2_choice == TrustGameActions.COOPERATE:
        player1_outcome = 3
        player2_outcome = -1
        return player1_outcome, player2_outcome
    elif player1_choice == TrustGameActions.COOPERATE and player2_choice == TrustGameActions.CHEAT:
        player1_outcome = -1
        player2_outcome = 3
        return player1_outcome, player2_outcome
    