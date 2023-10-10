from copy import deepcopy
from typing import Any, Dict, List
from trust.players import BasePlayer


class ScoreHandler:
    def __init__(self, players: List[BasePlayer]) -> None:
        self.scorecard = {player: 0 for player in players}

    def get_score(self, player: BasePlayer):
        return self.scorecard.get(player, 0)
    def update_scores(self, score: int, player: BasePlayer) -> None:
        self.scorecard[player] += score

    def reset_score(self, player: BasePlayer) -> None:
        self.scorecard[player] = 0

    def reset_scorecard(self):
        self.scorecard = {player: 0 for player in self.scorecard.keys()}

    def get_scores(self, players: List[BasePlayer]) -> Dict[BasePlayer, Dict[str, Any]]:
        scorecard = {player: self.scorecard[player] for player in players}
        return scorecard
    
    def get_scorecard(self):
        return self.scorecard
    
    def add_score_handlers(self, other_score_handler):
        if not isinstance(other_score_handler, ScoreHandler):
            raise TypeError('Parameter should be of the type ScoreHandler')

        for player in self.scorecard.keys():
            self.scorecard[player] += other_score_handler.get_score(player)
        
        return self