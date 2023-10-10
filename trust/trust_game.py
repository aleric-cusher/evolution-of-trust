from typing import List
import itertools
from trust.players import BasePlayer
from trust.actions import TrustGameActions
from trust.scorecard import Scorecard


class TrustGame:
    outcomes = {
        (TrustGameActions.CHEAT, TrustGameActions.CHEAT): (0, 0),
        (TrustGameActions.CHEAT, TrustGameActions.COOPERATE): (3, -1),
        (TrustGameActions.COOPERATE, TrustGameActions.CHEAT): (-1, 3),
        (TrustGameActions.COOPERATE, TrustGameActions.COOPERATE): (2, 2),    
    }

    def __init__(self, players: List[BasePlayer]) -> None:
        if players is not None:
            for player in players:
                if not isinstance(player, BasePlayer):
                    raise TypeError('Invalid player class.')

        self.players = players
        self.scorecard = Scorecard(self.players)
    
    def _play_game(self, player1: BasePlayer, player2: BasePlayer, num_games: int = 1) -> None:
        if not isinstance(num_games, int):
            raise TypeError('num_games should be of type int.')
        if num_games < 1:
            raise ValueError('Cannot play 0 or negative games.')
        
        for _ in range(num_games):
            scorecard = self.scorecard.get_scorecard([player1, player2])
            player1_action, player2_action = player1.action(scorecard), player2.action(scorecard)
            scores =  self.outcomes[(player1_action, player2_action)]
            self.scorecard.update_scores(scores[0], player1)
            self.scorecard.update_scores(scores[1], player2)
            self.scorecard.update_actions([player1_action], player1)
            self.scorecard.update_actions([player2_action], player2)
    
    def play_tournament(self, rounds_per_match: int = 10) -> None:
        for player1, player2 in itertools.combinations(self.players, 2):
            self._play_game(player1, player2, rounds_per_match)
            self.scorecard.reset_actions(player1)
            self.scorecard.reset_actions(player2)
