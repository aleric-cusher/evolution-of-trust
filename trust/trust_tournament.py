from typing import List
import itertools
from trust.scorecard import Scorecard
from trust.trust_game import TrustGame

from trust.players import BasePlayer


class TrustTournament:
    def __init__(self, players: List[BasePlayer]) -> None:
        if not isinstance(players, list):
            raise TypeError('players parameter is not of the type list')
        for player in players:
            if not isinstance(player, BasePlayer):
                raise TypeError('Invalid player class.')

        self.players = players
        self.scorecard = Scorecard(self.players)

    def play_tournament(self, rounds_per_match: int = 10) -> Scorecard:
        for player1, player2 in itertools.combinations(self.players, 2):
            game = TrustGame(player1, player2)
            new_score_card = game.play_game(rounds_per_match)

            self.scorecard.add_scores(new_score_card)
            game.end_game()
        return self.scorecard

