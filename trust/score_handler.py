from copy import deepcopy
from typing import Any, Dict, List
from trust.actions import TrustGameActions
from trust.players import BasePlayer


class ScoreHandler:
    def __init__(self, players: List[BasePlayer]) -> None:
        self.scorecard = {player: 0 for player in players}

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