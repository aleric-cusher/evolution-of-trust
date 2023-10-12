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

    def __init__(self, player1: BasePlayer, player2: BasePlayer) -> None:
        if not (isinstance(player1, BasePlayer) and isinstance(player2, BasePlayer)):
            raise TypeError('Invalid player class.')

        self.player1, self.player2 = player1, player2
        self.player1.new_game(player2)
        self.player2.new_game(player1)
        self.score_handler = Scorecard([self.player1, self.player2])
    
    def play_game(self, num_games: int = 1) -> Scorecard:
        if not isinstance(num_games, int):
            raise TypeError('num_games should be of type int.')
        if num_games < 1:
            raise ValueError('Cannot play 0 or negative games.')
        
        for _ in range(num_games):
            player1_action, player2_action = self.player1.action(), self.player2.action()
            scores =  self.outcomes[(player1_action, player2_action)]
            self.score_handler.update_scores(scores[0], self.player1)
            self.score_handler.update_scores(scores[1], self.player2)
        
        return self.score_handler


class TrustTournament:
    def __init__(self, players: List[BasePlayer]) -> None:
        if not isinstance(players, list):
            raise TypeError('players parameter is not of the type list')
        for player in players:
            if not isinstance(player, BasePlayer):
                raise TypeError('Invalid player class.')

        self.players = players
        self.score_handler = Scorecard(self.players)

    def play_tournament(self, rounds_per_match: int = 10) -> None:
        for player1, player2 in itertools.combinations(self.players, 2):
            game = TrustGame(player1, player2)
            new_score_handler = game.play_game(rounds_per_match)

            self.score_handler.add_score_handlers(new_score_handler)
        
        return self.score_handler

