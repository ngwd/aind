"""This file is provided as a starting template for writing your own unit
tests to run and debug your minimax and alphabeta agents locally.  The test
cases used by the project assistant are not public.
"""

import isolation
import game_agent
from importlib import reload
import unittest

class IsolationTest(unittest.TestCase):
    """Unit tests for isolation agents"""

    def setUp(self):
        reload(game_agent)
        self.player1 = "Player1"
        self.player2 = "Player2"
        self.game = isolation.Board(self.player1, self.player2)
        self.game._board_state = [
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                   0, 0, 0, 0, 0, 1, 0, 0, 0, 
                                   0, 0, 0, 1, 1, 1, 0, 0, 0, 
                                   0, 0, 0, 1, 1, 0, 0, 0, 0, 
                                   0, 0, 1, 1, 1, 1, 1, 0, 0, 
                                   0, 0, 0, 0, 1, 0, 0, 0, 0, 
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                   0, 0, 0, 0, 0, 0, 0, 0, 0, 
                                   0, 47, 32]
        self.depth = 3
        self.move = [7, 4]
        

    def test_solve(self):
        self.assertEqual(game_agent.MinimaxPlayer.get_move(self, self.game, 10000000), 
                         self.move)

if __name__ == '__main__':
    unittest.main()
