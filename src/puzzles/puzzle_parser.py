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
        last_move_uci = None
        last_move_san = None
        
        if pgn_str:
            try:
                # Use chess.pgn to parse properly (handles move numbers, comments, etc.)
                pgn_io = StringIO(pgn_str)
                game = chess.pgn.read_game(pgn_io)
                
                # Iterate through moves up to initialPly (inclusive)
                for i, move in enumerate(game.mainline_moves()):
                    if i > initial_ply:
                        break
                    
                    board.push(move)
                    if i == initial_ply:
                        last_move_uci = move.uci()
                        board.pop()
                        last_move_san = board.san(move)
                        board.push(move)
            except Exception as e:
                print(f"Error parsing PGN: {e}")
                # Fallback to simple splitting if pgn parsing fails
                board = chess.Board()
                moves = pgn_str.split()
                moves_pushed = 0
                
                for move_san in moves:
                    if moves_pushed > initial_ply:
                        break
                    try:
                        # Skip move numbers (e.g. "1.")
                        if move_san.endswith('.'):
                            continue
                            
                        move = board.push_san(move_san)
                        
                        if moves_pushed == initial_ply:
                            last_move_uci = move.uci()
                            last_move_san = move_san
                            
                        moves_pushed += 1
                    except:
                        pass
        
        return {
            'id': puzzle.get('id', 'unknown'),
            'fen': board.fen(),
            'moves': puzzle.get('solution', []),
            'rating': puzzle.get('rating', 1500),
            'themes': puzzle.get('themes', []),
            'pgn': pgn_str,
            'last_move_uci': last_move_uci,
            'last_move_san': last_move_san
        }
    
    @staticmethod
    def parse_solution_moves(moves_list):
        """Convert solution moves list to chess.Move objects"""
        return moves_list
