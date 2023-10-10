
from trust.actions import TrustGameActions
from trust.scorecard import Scorecard
from trust.players import RandomPlayer, AlwaysCheatPlayer, AlwaysCooperatePlayer


class TestScorecard:
    def test_creation(self):
        players = [RandomPlayer(), AlwaysCheatPlayer(), AlwaysCooperatePlayer()]
        try:
            scorecard = Scorecard(players)
            assert True
        except Exception as e:
            assert False, e
        
    def test_scorecard_attributes(self):
        player1 = RandomPlayer()
        scorecard = Scorecard((player1,))

        assert scorecard.scorecard[player1]['score'] == 0
        assert scorecard.scorecard[player1]['actions'] == []

    def test_scorecard_update_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard((player1, player2)) 

        scorecard.update_scores(33, player1)
        scorecard.update_scores(25, player2)
        
        assert scorecard.scorecard[player1]['score'] == 33
        assert scorecard.scorecard[player2]['score'] == 25
    
    def test_scorecard_update_actions(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard((player1, player2))
        
        assert scorecard.scorecard[player1]['actions'] == []
        assert scorecard.scorecard[player2]['actions'] == []

        scorecard.update_actions([TrustGameActions.CHEAT], player1)
        scorecard.update_actions([TrustGameActions.COOPERATE], player2)

        assert scorecard.scorecard[player1]['actions'] == [TrustGameActions.CHEAT]
        assert scorecard.scorecard[player2]['actions'] == [TrustGameActions.COOPERATE]

    def test_reset_actions(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard((player1, player2))
        scorecard.scorecard = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]}
        }

        scorecard.reset_actions(player1)

        assert scorecard.scorecard[player1]['actions'] == []
        assert scorecard.scorecard[player1]['score'] == 5
        assert scorecard.scorecard[player2]['actions'] == [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]
        assert scorecard.scorecard[player2]['score'] == 6
        
    def test_reset_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard((player1, player2))
        scorecard.scorecard = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]}
        }

        scorecard.reset_score(player1)

        assert scorecard.scorecard[player1]['actions'] == [TrustGameActions.CHEAT, TrustGameActions.CHEAT]
        assert scorecard.scorecard[player1]['score'] == 0
        assert scorecard.scorecard[player2]['actions'] == [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]
        assert scorecard.scorecard[player2]['score'] == 6

    def test_reset_scorecard(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard((player1, player2))
        scorecard.scorecard = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]}
        }

        scorecard.reset_scorecard()

        assert scorecard.scorecard[player1]['actions'] == []
        assert scorecard.scorecard[player1]['score'] == 0
        assert scorecard.scorecard[player2]['actions'] == []
        assert scorecard.scorecard[player2]['score'] == 0
    
    def test_get_scorecard(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        scorecard = Scorecard((player1, player2, player3))
        scorecard.scorecard = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]},
            player3: {'score': 2, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]}
        }

        scorecard_object = scorecard.get_scorecard([player1, player2, player3])
        assert scorecard_object == {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]},
            player3: {'score': 2, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]}
        }

        scorecard_object = scorecard.get_scorecard([player1, player2])
        assert scorecard_object == {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]},
        }

        scorecard_object = scorecard.get_scorecard([player1])
        assert scorecard_object == {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
        }