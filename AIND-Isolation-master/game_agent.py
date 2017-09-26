"""Finish all TODO items in this file to complete the isolation project, then
test your agent's strength against a set of known agents using tournament.py
and include the results in your report.
"""
import random

class SearchTimeout(Exception):
    """Subclass base exception for code clarity. """
    pass


def custom_score(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    """
    nleaf = len(game.get_legal_moves())
    return float(-nleaf) if player==game._player_1 else float(nleaf)
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own = len(game.get_legal_moves(player))
    opp = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own*own - opp*opp)
    #return float(2.5*own - opp)

def custom_score_2(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    This should be the best heuristic function for your project submission.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    """
    nleaf  = len(game.get_legal_moves())
    nleaf2 = len(game.get_legal_moves(game._player_2))
    return float(nleaf2-nleaf) if player==game._player_1 else float(nleaf-nleaf2)
    """

    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own = len(game.get_legal_moves(player))
    opp = len(game.get_legal_moves(game.get_opponent(player)))
    return float(own - opp)

def custom_score_3(game, player):
    """Calculate the heuristic value of a game state from the point of view
    of the given player.

    Note: this function should be called from within a Player instance as
    `self.score()` -- you should not need to call this function directly.

    Parameters
    ----------
    game : `isolation.Board`
        An instance of `isolation.Board` encoding the current state of the
        game (e.g., player locations and blocked cells).

    player : object
        A player instance in the current game (i.e., an object corresponding to
        one of the player objects `game.__player_1__` or `game.__player_2__`.)

    Returns
    -------
    float
        The heuristic value of the current game state to the specified player.
    """
    """
    nleaf = len(game.get_legal_moves())
    nleaf2 = len(game.get_legal_moves(game._player_2))
    return float(nleaf2-2*nleaf) if player==game._player_1 else float(2*nleaf-nleaf2)
    """
    if game.is_loser(player):
        return float("-inf")

    if game.is_winner(player):
        return float("inf")

    own = len(game.get_legal_moves(player))
    opp = len(game.get_legal_moves(game.get_opponent(player)))
    return float(2*own- opp)

class IsolationPlayer:
    """Base class for minimax and alphabeta agents -- this class is never
    constructed or tested directly.

    ********************  DO NOT MODIFY THIS CLASS  ********************

    Parameters
    ----------
    search_depth : int (optional)
        A strictly positive integer (i.e., 1, 2, 3,...) for the number of
        layers in the game tree to explore for fixed-depth search. (i.e., a
        depth of one (1) would only explore the immediate sucessors of the
        current state.)

    score_fn : callable (optional)
        A function to use for heuristic evaluation of game states.

    timeout : float (optional)
        Time remaining (in milliseconds) when search is aborted. Should be a
        positive value large enough to allow the function to return before the
        timer expires.
    """
    def __init__(self, search_depth=3, score_fn=custom_score, timeout=10., game=None):
        self.search_depth = search_depth
        self.score = score_fn
        self.time_left = None
        self.TIMER_THRESHOLD = timeout

    def get_move(self, game, time_left):
        """Search for the best move from the available legal moves and return a
        result before the time limit expires.

        **************  YOU DO NOT NEED TO MODIFY THIS FUNCTION  *************

        For fixed-depth search, this function simply wraps the call to the
        minimax method, but this method provides a common interface for all
        Isolation agents, and you will replace it in the AlphaBetaPlayer with
        iterative deepening search.

        Parameters
        ----------
        game : `isolation.Board`
            An instance of `isolation.Board` encoding the current state of the
            game (e.g., player locations and blocked cells).

        time_left : callable
            A function that returns the number of milliseconds left in the
            current turn. Returning with any less than 0 ms remaining forfeits
            the game.

        Returns
        -------
        (int, int)
            Board coordinates corresponding to a legal move; may return
            (-1, -1) if there are no available legal moves.
        """
        self.time_left = time_left

        # Initialize the best move so that this function returns something
        # in case the search fails due to timeout
        best_move = (-1, -1)

        try:
            # The try/except block will automatically catch the exception
            # raised when the timer is about to expire.
            depth = self.search_depth
            if type(self).__name__=="MinimaxPlayer":
                while depth < game.width * game.height:
                    best_move = self.minimax(game, depth)
                    depth += 1
            else:
                while depth < game.width * game.height:
                    best_move = self.alphabeta(game, depth)
                    depth += 1
        except SearchTimeout:
            pass

        if best_move == (-1, -1):
            legal_moves = game.get_legal_moves()
            if len(legal_moves) : 
                best_move = legal_moves[random.randint(0, len(legal_moves) - 1)]

        # Return the best move from the last completed search iteration
        return best_move
class MinimaxPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using depth-limited minimax
    search. You must finish and test this player to make sure it properly uses
    minimax to return a good move before the search time limit expires.
    """
    
    def minimax(self, game, depth):
        """Implement depth-limited minimax search algorithm as described in
        the lectures.

        This should be a modified version of MINIMAX-DECISION in the AIMA text.
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Minimax-Decision.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        move = (-1, -1)
        legal_moves = game.get_legal_moves()
        if len(legal_moves)==0: 
            return move 
        score_i, move = max ((self.min_value(game, p, depth-1), p) for p in legal_moves )
        return move

    def min_value(self, game, move, depth):
        """Implement the min part of minimax search algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        move: (int, int)
            a move not yet apply on the Board, need forcast this move on Board first

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
        float 
        """
        if self.time_left()<self.TIMER_THRESHOLD : 
            raise SearchTimeout()
        game_tmp = game.forecast_move(move)
        
        legal_moves = game_tmp.get_legal_moves()
        score_i = float("inf")

        if depth==0 : 
            #return self.score(game_tmp, game_tmp._player_1) 
            return self.score(game_tmp, self) 

        for p in legal_moves:
            score_i = min(score_i, self.max_value(game_tmp, p, depth-1))
        return score_i

    def max_value(self, game, move, depth):
        """Implement the max part of minimax search algorithm

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        move: (int, int)
            a move not yet apply on the Board, need forcast this move on Board first

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        Returns
        -------
           float
        """
        if self.time_left()<self.TIMER_THRESHOLD : 
            raise SearchTimeout()
        game_tmp = game.forecast_move(move)

        legal_moves = game_tmp.get_legal_moves()
        score_i = float("-inf")

        if depth==0 : 
            #return self.score(game_tmp, game_tmp._player_2) 
            return self.score(game_tmp, self) 

        for p in legal_moves:
            score_i = max(score_i, self.min_value(game_tmp, p, depth-1))
        return score_i

class AlphaBetaPlayer(IsolationPlayer):
    """Game-playing agent that chooses a move using iterative deepening minimax
    search with alpha-beta pruning. You must finish and test this player to
    make sure it returns a good move before the search time limit expires.
    """

    def alphabeta(self, game, depth, alpha=float("-inf"), beta=float("inf")):
        """Implement depth-limited minimax search with alpha-beta pruning as
        described in the lectures.

        This should be a modified version of ALPHA-BETA-SEARCH in the AIMA text
        https://github.com/aimacode/aima-pseudocode/blob/master/md/Alpha-Beta-Search.md

        **********************************************************************
            You MAY add additional methods to this class, or define helper
                 functions to implement the required functionality.
        **********************************************************************

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state

        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting

        alpha : float
            Alpha limits the lower bound of search on minimizing layers

        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        (int, int)
            The board coordinates of the best move found in the current search;
            (-1, -1) if there are no legal moves

        Notes
        -----
            (1) You MUST use the `self.score()` method for board evaluation
                to pass the project tests; you cannot call any other evaluation
                function directly.

            (2) If you use any helper functions (e.g., as shown in the AIMA
                pseudocode) then you must copy the timer check into the top of
                each helper function or else your agent will timeout during
                testing.
        """
        if self.time_left() < self.TIMER_THRESHOLD:
            raise SearchTimeout()
        score_i, move = float("-inf"), (-1, -1)
        legal_moves = game.get_legal_moves()
        for v in legal_moves : 
            tmp = self.min_value(game, v, alpha, beta, depth-1)
            if tmp > score_i:
                score_i, move, alpha = tmp, v, tmp
        return move

    def min_value(self, game, move, alpha, beta, depth):
        """Implement depth-limited min part of alpha-beta pruning as
        described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        move : tuple
            the move will be forecast on the board
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            the utility/score of this move, 
        Notes
        -----
            
        """
        if self.time_left()<self.TIMER_THRESHOLD : 
            raise SearchTimeout()
        game_tmp = game.forecast_move(move)
        
        legal_moves = game_tmp.get_legal_moves()
        score_i = float("inf")

        if depth==0 : 
            return self.score(game_tmp, self) 

        for v in legal_moves:
            score_i = min(score_i, self.max_value(game_tmp, v, alpha, beta, depth-1))
            if score_i <= alpha:
                return score_i
            beta = min (beta, score_i)
        return score_i

    def max_value(self, game, move, alpha, beta, depth):
        """Implement depth-limited max part of alpha-beta pruning as
        described in the lectures.

        Parameters
        ----------
        game : isolation.Board
            An instance of the Isolation game `Board` class representing the
            current game state
        move : tuple
            the move will be forecast on the board
        depth : int
            Depth is an integer representing the maximum number of plies to
            search in the game tree before aborting
        alpha : float
            Alpha limits the lower bound of search on minimizing layers
        beta : float
            Beta limits the upper bound of search on maximizing layers

        Returns
        -------
        float
            the utility/score of this move, 
        Notes
        -----
            
        """
        if self.time_left()<self.TIMER_THRESHOLD : 
            raise SearchTimeout()
        game_tmp = game.forecast_move(move)
        
        legal_moves = game_tmp.get_legal_moves()
        score_i = float("-inf")

        if depth==0 : 
            return self.score(game_tmp, self) 

        for v in legal_moves:
            score_i = max(score_i, self.min_value(game_tmp, v, alpha, beta, depth-1))
            if score_i >= beta:
                return score_i
            alpha = max(alpha, score_i)
        return score_i

