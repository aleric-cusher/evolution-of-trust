import pytest
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
        scorecard = Scorecard([player1])

        assert player1 in scorecard._scorecard.keys()

    def test_get_score(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        scorecard = Scorecard([player1, player2, player3])
        test_card = {
            player1: {'score': 5, 'actions': []},
            player2: {'score': 6, 'actions': []},
            player3: {'score': 2, 'actions': []},
        }

        scorecard._scorecard = test_card
        
        assert scorecard.get_score(player2) == 6
        assert scorecard.get_score(player3) == 2
        assert scorecard.get_score(player1) == 5

    def test_update_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard([player1, player2]) 

        scorecard.update_score(33, player1)
        scorecard.update_score(25, player2)
        
        assert scorecard.get_score(player1) == 33
        assert scorecard.get_score(player2) == 25
        
    def test_reset_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard([player1, player2])
        
        scorecard.update_score(45, player1)
        scorecard.update_score(6, player2)
        scorecard.reset_score(player1)

        assert scorecard.get_score(player1) == 0
        assert scorecard.get_score(player2) == 6

    def test_get_actions(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        scorecard = Scorecard([player1, player2, player3])
        test_card = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]},
            player3: {'score': 2, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]},
        }

        scorecard._scorecard = test_card
        
        assert scorecard.get_actions(player2) == [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]
        assert scorecard.get_actions(player3) == [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]
        assert scorecard.get_actions(player1) == [TrustGameActions.CHEAT, TrustGameActions.CHEAT]

    def test_update_actions(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard([player1, player2]) 

        scorecard.update_actions(TrustGameActions.CHEAT, player1)
        scorecard.update_actions(TrustGameActions.COOPERATE, player2)
        
        assert scorecard.get_actions(player1) == [TrustGameActions.CHEAT]
        assert scorecard.get_actions(player2) == [TrustGameActions.COOPERATE]

    def test_reset_actions(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard([player1, player2]) 

        scorecard.update_actions(TrustGameActions.CHEAT, player1)
        scorecard.update_actions(TrustGameActions.COOPERATE, player2)
        
        scorecard.reset_actions(player1)
        
        assert scorecard.get_actions(player1) == []
        assert scorecard.get_actions(player2) == [TrustGameActions.COOPERATE]
    
    def test_get_scorecard(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        scorecard = Scorecard([player1, player2, player3])
        test_card = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]},
            player3: {'score': 2, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.CHEAT]},
        }

        scorecard._scorecard = test_card
        scorecard_object = scorecard.get_scorecard()
        
        assert scorecard_object == test_card
        
    def test_reset_scorecard(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        scorecard = Scorecard([player1, player2])
        test_card = {
            player1: {'score': 5, 'actions': [TrustGameActions.CHEAT, TrustGameActions.CHEAT]},
            player2: {'score': 6, 'actions': [TrustGameActions.COOPERATE, TrustGameActions.COOPERATE]},
        }

        scorecard._scorecard = test_card
        scorecard.reset_scorecard()

        assert scorecard._scorecard == {
            player1: {'score': 0, 'actions': []},
            player2: {'score': 0, 'actions': []},
        }

    def test_add_scores(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        scorecard = Scorecard([player1, player2, player3])
        scorecard._scorecard = {
            player1: {'score': 5, 'actions': []},
            player2: {'score': 6, 'actions': []},
            player3: {'score': 2, 'actions': []},
        }

        scorecard2 = Scorecard([player1, player3])
        scorecard2._scorecard = {
            player1: {'score': -3, 'actions': []},
            player3: {'score': 8, 'actions': []}
        }

        expected_scorecard = {
            player1: {'score': 2, 'actions': []},
            player2: {'score': 6, 'actions': []},
            player3: {'score': 10, 'actions': []}
        }

        scorecard3 = scorecard.add_scores(scorecard2)
        
        assert scorecard3.get_scorecard() == expected_scorecard
    
    def test_invalid_type_handler(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        scorecard = Scorecard([player1, player2, player3])
        with pytest.raises(TypeError):
            scorecard3 = scorecard.add_scores('score_handler2')