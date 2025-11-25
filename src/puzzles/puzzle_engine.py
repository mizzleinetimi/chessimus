"""Puzzle validation and solution checking"""

import chess

class PuzzleEngine:
    """Handle puzzle logic and validation"""
    
    def __init__(self, puzzle_data):
        """Initialize with parsed puzzle data"""
        self.puzzle_data = puzzle_data
        self.board = chess.Board(puzzle_data['fen'])
        self.solution_moves = puzzle_data['moves']
        self.current_move_index = 0
        self.completed = False
    
    def check_move(self, move_str):
        """
        Check if user move matches solution
        Returns: ('correct', move) or ('incorrect', None) or ('complete', None)
        """
        if self.completed:
            return ('complete', None)
        
        try:
            # Parse user move
            try:
                user_move = self.board.parse_san(move_str)
            except:
                user_move = chess.Move.from_uci(move_str)
            
            # Get expected move
            expected_uci = self.solution_moves[self.current_move_index]
            expected_move = chess.Move.from_uci(expected_uci)
            
            if user_move == expected_move:
                self.board.push(user_move)
                self.current_move_index += 1
                
                # Make opponent's response if available
                if self.current_move_index < len(self.solution_moves):
                    opponent_uci = self.solution_moves[self.current_move_index]
                    opponent_move = chess.Move.from_uci(opponent_uci)
                    self.board.push(opponent_move)
                    self.current_move_index += 1
                
                # Check if puzzle complete
                if self.current_move_index >= len(self.solution_moves):
                    self.completed = True
                    return ('complete', user_move)
                
                return ('correct', user_move)
            else:
                return ('incorrect', None)
        
        except Exception as e:
            return ('error', str(e))
    
    def get_board(self):
        """Get current board state"""
        return self.board
    
    def is_complete(self):
        """Check if puzzle is solved"""
        return self.completed
    
    def get_hint(self):
        """Get next expected move as hint"""
        if self.current_move_index < len(self.solution_moves):
            move_uci = self.solution_moves[self.current_move_index]
            move = chess.Move.from_uci(move_uci)
            return self.board.san(move)
        return None
    
    def get_turn_info(self):
        """Get whose turn it is"""
        return "White" if self.board.turn else "Black"
    
    def get_moves_from_square(self, square_str):
        """
        Get legal moves from a specific square (e.g., 'e2')
        Returns (list of moves in SAN, list of destination squares), or (None, None) if invalid
        """
        try:
            # Parse square (e.g., 'e2' -> chess.E2)
            square = chess.parse_square(square_str)
            
            # Get piece on that square
            piece = self.board.piece_at(square)
            if not piece:
                return None, None
            
            # Get all legal moves from this square
            moves_from_square = []
            dest_squares = []
            for move in self.board.legal_moves:
                if move.from_square == square:
                    moves_from_square.append(self.board.san(move))
                    dest_squares.append(move.to_square)
            
            if moves_from_square:
                return moves_from_square, dest_squares
            return None, None
        except:
            return None, None
