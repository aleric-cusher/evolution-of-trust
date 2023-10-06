from enum import Enum

class TrustGameActions(Enum):
    CHEAT = 0


def play_game(player1_choice, player2_choice):
    if player1_choice == TrustGameActions.CHEAT and player2_choice == TrustGameActions.CHEAT:
        player1_outcome = 0
        player2_outcome = 0
        return player1_outcome, player2_outcome