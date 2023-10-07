from trust.players import BasePlayer
from trust.actions import TrustGameActions


class TrustGame:
    outcomes = {
        (TrustGameActions.CHEAT, TrustGameActions.CHEAT): (0, 0),
        (TrustGameActions.CHEAT, TrustGameActions.COOPERATE): (3, -1),
        (TrustGameActions.COOPERATE, TrustGameActions.CHEAT): (-1, 3),
        (TrustGameActions.COOPERATE, TrustGameActions.COOPERATE): (2, 2),    
    }

    def __init__(self, player1: BasePlayer, player2: BasePlayer) -> None:
        if not (isinstance(player1, BasePlayer) and isinstance(player2, BasePlayer)):
            raise TypeError('Invalid player class.')

        self.player1 = player1
        self.player2 = player2
        self.player1_score = 0
        self.player2_score = 0

    def update_player_score(self, scores):
        self.player1_score += scores[0]
        self.player2_score += scores[1]
    
    def play_game(self, num_games: int = 1) -> None:
        if not isinstance(num_games, int):
            raise TypeError('num_games should be of type int.')
        if num_games < 1:
            raise ValueError('Cannot play 0 or negative games.')
        
        for _ in range(num_games):
            scores =  self.outcomes[(self.player1.action(), self.player2.action())]
            self.update_player_score(scores)
            
        