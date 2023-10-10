from typing import Any, Dict, List
from trust.actions import TrustGameActions
from trust.players import BasePlayer


class Scorecard:
    def __init__(self, players: List[BasePlayer]) -> None:
        self.scorecard = {player: {'score': 0, 'actions': []} for player in players}

    def update_scores(self, score: int, player: BasePlayer) -> None:
        self.scorecard[player]['score'] += score
    
    def update_actions(self, actions: List[TrustGameActions], player: BasePlayer) -> None:
        self.scorecard[player]['actions'].extend(actions)

    def reset_actions(self, player: BasePlayer) -> None:
        self.scorecard[player]['actions'] = []

    def reset_score(self, player: BasePlayer) -> None:
        self.scorecard[player]['score'] = 0

    def reset_scorecard(self):
        self.scorecard = {player: {'score': 0, 'actions': []} for player in self.scorecard.keys()}

    def get_scorecard(self, players: List[BasePlayer]) -> Dict[BasePlayer, Dict[str, Any]]:
        scorecard = {player: self.scorecard[player] for player in players}
        return scorecard