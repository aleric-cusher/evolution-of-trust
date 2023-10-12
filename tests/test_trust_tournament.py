import pytest
from trust.trust_tournament import TrustTournament
from trust.players import AlwaysCooperatePlayer, DetectivePlayer, AlwaysCheatPlayer, CopycatPlayer, GrudgePlayer


class TestTrustTournament:
    def test_tournament_attributes(self):
        players = [AlwaysCheatPlayer(), AlwaysCooperatePlayer(), DetectivePlayer()]
        tourney = TrustTournament(players)
        
        assert players[0] in tourney.players
        assert players[1] in tourney.players
        assert players[2] in tourney.players
    
    def test_invalid_player_tuple(self):
        with pytest.raises(TypeError):
            players = (AlwaysCheatPlayer(), AlwaysCooperatePlayer(), DetectivePlayer())
            tourney = TrustTournament(players)
    
    def test_invalid_player(self):
        with pytest.raises(TypeError):
            players = [AlwaysCheatPlayer(), 'm', 8]
            tourney = TrustTournament(players)
    

class TestTwoPlayerTournament:
    parameters = [
        # (player1_class, player2_class, rounds_per_match, player1_score, player2_score)
        (CopycatPlayer, AlwaysCooperatePlayer, 10, 20, 20),
        (CopycatPlayer, AlwaysCheatPlayer, 10, -1, 3),
        (GrudgePlayer, AlwaysCheatPlayer, 10, -1, 3),        
        (GrudgePlayer, AlwaysCooperatePlayer, 10, 20, 20),
        (GrudgePlayer, CopycatPlayer, 10, 20, 20),
        (DetectivePlayer, CopycatPlayer, 10, 18, 18),
        (DetectivePlayer, AlwaysCheatPlayer, 10, -3, 9),
        (DetectivePlayer, AlwaysCooperatePlayer, 10, 27, -1),
        (DetectivePlayer, GrudgePlayer, 10, 3, 7),
    ]

    @pytest.mark.parametrize('player1_class, player2_class, rounds_per_match, player1_score, player2_score', parameters)
    def test_tournament_between_two_players(self, player1_class, player2_class, rounds_per_match, player1_score, player2_score):
        players = [player1_class(), player2_class()]
        tourney = TrustTournament(players)
        tourney.play_tournament(rounds_per_match)

        assert tourney.scorecard.get_score(players[0]) == player1_score
        assert tourney.scorecard.get_score(players[1]) == player2_score
    

class TestMultiplePlayersTournament:
    def test_5_different_players(self):
        players = [CopycatPlayer(), AlwaysCheatPlayer(), AlwaysCooperatePlayer(), GrudgePlayer(), DetectivePlayer()]
        tourney = TrustTournament(players)
        scorecard = tourney.play_tournament()
        
        assert scorecard.get_score(players[0]) == 57
        assert scorecard.get_score(players[1]) == 45
        assert scorecard.get_score(players[2]) == 29
        assert scorecard.get_score(players[3]) == 46
        assert scorecard.get_score(players[4]) == 45
