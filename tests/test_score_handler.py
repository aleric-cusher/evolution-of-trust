
from trust.actions import TrustGameActions
from trust.score_handler import ScoreHandler
from trust.players import RandomPlayer, AlwaysCheatPlayer, AlwaysCooperatePlayer


class TestScoreHandler:
    def test_creation(self):
        players = [RandomPlayer(), AlwaysCheatPlayer(), AlwaysCooperatePlayer()]
        try:
            score_handler = ScoreHandler(players)
            assert True
        except Exception as e:
            assert False, e
        
    def test_scorecard_attributes(self):
        player1 = RandomPlayer()
        score_handler = ScoreHandler([player1])

        assert score_handler.scorecard[player1] == 0

    def test_scorecard_update_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        score_handler = ScoreHandler([player1, player2]) 

        score_handler.update_scores(33, player1)
        score_handler.update_scores(25, player2)
        
        assert score_handler.scorecard[player1] == 33
        assert score_handler.scorecard[player2] == 25
        
    def test_reset_score(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        score_handler = ScoreHandler([player1, player2])
        score_handler.scorecard = {
            player1: 5,
            player2: 6
        }
        score_handler.reset_score(player1)

        assert score_handler.scorecard[player1] == 0
        assert score_handler.scorecard[player2] == 6

    def test_reset_scorecard(self):
        player1, player2 = AlwaysCheatPlayer(), AlwaysCooperatePlayer()
        score_handler = ScoreHandler([player1, player2])
        score_handler.scorecard = {
            player1: 5,
            player2: 6
        }

        score_handler.reset_scorecard()

        assert score_handler.scorecard[player1] == 0
        assert score_handler.scorecard[player2] == 0
    
    def test_get_scores(self):
        player1, player2, player3 = AlwaysCheatPlayer(), AlwaysCooperatePlayer(), RandomPlayer()
        score_handler = ScoreHandler([player1, player2, player3])
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
        score_handler = ScoreHandler([player1, player2, player3])
        test_card = {
            player1: 5,
            player2: 6,
            player3: 2,
        }

        score_handler.scorecard = test_card
        scorecard_object = score_handler.get_scorecard()
        
        assert scorecard_object == test_card

        
    