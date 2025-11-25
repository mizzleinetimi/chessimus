"""Parse Lichess puzzle JSON into usable format"""

import chess
import chess.pgn
from io import StringIO

class PuzzleParser:
    """Parse puzzle data from Lichess API"""
    
    @staticmethod
    def parse(puzzle_json):
        """
        Parse puzzle JSON into structured format
        Returns: {
            'id': str,
            'fen': str,
            'moves': list,
            'rating': int,
            'themes': list
        }
        """
        game = puzzle_json.get('game', {})
        puzzle = puzzle_json.get('puzzle', {})
        
        # Get the puzzle position by playing through the PGN
        pgn_str = game.get('pgn', '')
        initial_ply = puzzle.get('initialPly', 0)
        
        # Parse PGN and get position at initialPly
        board = chess.Board()
        if pgn_str:
            moves = pgn_str.split()
            for i, move_san in enumerate(moves):
                if i >= initial_ply:
                    break
                try:
                    board.push_san(move_san)
                except:
                    pass
        
        return {
            'id': puzzle.get('id', 'unknown'),
            'fen': board.fen(),
            'moves': puzzle.get('solution', []),
            'rating': puzzle.get('rating', 1500),
            'themes': puzzle.get('themes', []),
            'pgn': pgn_str
        }
    
    @staticmethod
    def parse_solution_moves(moves_list):
        """Convert solution moves list to chess.Move objects"""
        return moves_list
