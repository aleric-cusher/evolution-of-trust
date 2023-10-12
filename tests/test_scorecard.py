import pytest
from trust.actions import TrustGameActions
from trust.scorecard import Scorecard
from trust.players import RandomPlayer, AlwaysCheatPlayer, AlwaysCooperatePlayer


class TestScorecard:
    def test_creation(self):
        players = [RandomPlayer(), AlwaysCheatPlayer(), AlwaysCooperatePlayer()]
        try:
            score_handler = Scorecard(players)
            assert True
        except Exception as e:
            assert False, e
        
    def test_scorecard_attributes(self):
        player1 = RandomPlayer()
        score_handler = Scorecard([player1])

        assert score_handler.scorecard[player1] == 0

    def test_scorecard_update_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        score_handler = Scorecard([player1, player2]) 

        score_handler.update_scores(33, player1)
        score_handler.update_scores(25, player2)
        
        assert score_handler.scorecard[player1] == 33
        assert score_handler.scorecard[player2] == 25
        
    def test_reset_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        score_handler = Scorecard([player1, player2])
        score_handler.scorecard = {
            player1: 5,
            player2: 6
        }
        score_handler.reset_score(player1)

        assert score_handler.scorecard[player1] == 0
        assert score_handler.scorecard[player2] == 6

    def test_reset_scorecard(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        score_handler = Scorecard([player1, player2])
        score_handler.scorecard = {
            player1: 5,
            player2: 6
        }

        score_handler.reset_scorecard()

        assert score_handler.scorecard[player1] == 0
        assert score_handler.scorecard[player2] == 0
    
    def test_get_scores(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        score_handler = Scorecard([player1, player2, player3])
        test_card = {
            player1: 5,
            player2: 6,
            player3: 2,
        }

        score_handler.scorecard = test_card

        scorecard_object = score_handler.get_scores([player3, player2])
        assert scorecard_object[player2] == 6
        assert scorecard_object[player3] == 2
        assert player1 not in scorecard_object.keys()
    
    def test_get_scorecard(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        score_handler = Scorecard([player1, player2, player3])
        test_card = {
            player1: 5,
            player2: 6,
            player3: 2,
        }

        score_handler.scorecard = test_card
        scorecard_object = score_handler.get_scorecard()
        
        assert scorecard_object == test_card

    def test_add_scores(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        score_handler1 = Scorecard([player1, player2, player3])
        score_handler1.scorecard = {
            player1: 5,
            player2: 6,
            player3: 2,
        }

        score_handler2 = Scorecard([player1, player3])
        score_handler2.scorecard = {
            player1: -3,
            player3: 8
        }

        expected_scorecard = {
            player1: 2,
            player2: 6,
            player3: 10
        }

        score_handler3 = score_handler1.add_score_handlers(score_handler2)
        
        assert score_handler3.get_scorecard() == expected_scorecard
    
    def test_invalid_type_handler(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        score_handler1 = Scorecard([player1, player2, player3])
        with pytest.raises(TypeError):
            score_handler3 = score_handler1.add_score_handlers('score_handler2')