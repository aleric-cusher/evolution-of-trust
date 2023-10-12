from copy import deepcopy, copy
from typing import Any, Dict, List
from trust.actions import TrustGameActions
from trust.players import BasePlayer


class Scorecard:
    def __init__(self, players: List[BasePlayer]) -> None:
        self._scorecard = {player: {'score': 0, 'actions': []} for player in players}

    def get_card(self, player: BasePlayer):
        return deepcopy(self._scorecard.get(player, None))

    def get_score(self, player: BasePlayer) -> Dict[BasePlayer, Dict[str, Any]]:
        return self._scorecard[player]['score']
    
    def update_score(self, score: int, player: BasePlayer) -> None:
        self._scorecard[player]['score'] += score

    def reset_score(self, player: BasePlayer) -> None:
        self._scorecard[player]['score'] = 0
    
    def get_actions(self, player: BasePlayer) -> List[TrustGameActions]:
        return copy(self._scorecard[player]['actions'])
    
    def update_actions(self, action: TrustGameActions, player: BasePlayer) -> None:
        self._scorecard[player]['actions'].append(action)

    def reset_actions(self, player: BasePlayer) -> None:
        self._scorecard[player]['actions'] = []

    def get_scorecard(self):
        return copy(self._scorecard)
    
    def reset_scorecard(self):
        self._scorecard = {player: {'score': 0, 'actions': []} for player in self._scorecard.keys()}
    
    def add_scores(self, other_scorecard):
        if not isinstance(other_scorecard, Scorecard):
            raise TypeError('Parameter should be of the type ScoreHandler')

        for player in other_scorecard.get_scorecard().keys():
            self.update_score(other_scorecard.get_score(player), player)
        
        return self