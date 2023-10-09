from typing import Optional, Iterable, Any
from trust.players import BasePlayer
from trust.actions import TrustGameActions
import itertools


class TrustGame:
    outcomes = {
        (TrustGameActions.CHEAT, TrustGameActions.CHEAT): (0, 0),
        (TrustGameActions.CHEAT, TrustGameActions.COOPERATE): (3, -1),
        (TrustGameActions.COOPERATE, TrustGameActions.CHEAT): (-1, 3),
        (TrustGameActions.COOPERATE, TrustGameActions.COOPERATE): (2, 2),    
    }

    def __init__(self, players:Optional[list[BasePlayer]] = None) -> None:
        if players is not None:
            for player in players:
                if not isinstance(player, BasePlayer):
                    raise TypeError('Invalid player class.')

        self.players = players
        self.scorecard = {player: {'score': 0, 'actions': []} for player in self.players}
    
    def _get_player_combinations(self) -> Iterable[Iterable[BasePlayer]]:
        unique_combinations = []
        for combination in itertools.combinations(self.players, 2):
            unique_combinations.append(combination)
        return unique_combinations
    
    def _get_scorecard(self, player1: BasePlayer, player2: BasePlayer) -> dict[BasePlayer, dict[str, Any]]:
        return {
            player1: self.scorecard[player1],
            player2: self.scorecard[player2]
        }

    def update_player_scores(self, scores: Iterable[int], player1: BasePlayer, player2: BasePlayer) -> None:
        self.scorecard[player1]['score'] += scores[0]
        self.scorecard[player2]['score'] += scores[1]

    def update_player_actions(self, actions: Iterable[TrustGameActions], player1: BasePlayer, player2: BasePlayer) -> None:
        self.scorecard[player1]['actions'].append(actions[0])
        self.scorecard[player2]['actions'].append(actions[1])
    
    def play_2_players(self, player1: BasePlayer, player2: BasePlayer) -> None:
        scorecard = self._get_scorecard(player1, player2)
        player1_action, player2_action = player1.action(scorecard), player2.action(scorecard)
        scores =  self.outcomes[(player1_action, player2_action)]
        self.update_player_scores(scores, player1, player2)
        self.update_player_actions((player1_action, player2_action), player1, player2)
    
    def play_game(self, num_games: int = 1) -> None:
        if not isinstance(num_games, int):
            raise TypeError('num_games should be of type int.')
        if num_games < 1:
            raise ValueError('Cannot play 0 or negative games.')
        
        for _ in range(num_games):
            for player1, player2 in self._get_player_combinations():
                self.play_2_players(player1, player2)
