"""Chess engine wrapper using python-chess"""

import chess

class ChessEngine:
    """Wrapper for chess rules and board state"""
    
    def __init__(self, fen=None):
        """Initialize board with optional FEN"""
        self.board = chess.Board(fen) if fen else chess.Board()
        self.move_history = []
    
    def get_moves_from_square(self, square_str):
        """
        Get all legal moves from a specific square
        Args: square_str like 'e2', 'g1', etc.
        Returns: list of moves in SAN notation, or None if invalid square
        """
        try:
            square = chess.parse_square(square_str)
            piece = self.board.piece_at(square)
            
            if piece is None:
                return None
            
            # Get all legal moves from this square
            moves_from_square = []
            for move in self.board.legal_moves:
                if move.from_square == square:
                    moves_from_square.append(self.board.san(move))
            
            return moves_from_square if moves_from_square else None
        except:
            return None
    
    def make_move(self, move_str):
        """
        Make a move from string (e.g., 'e4', 'Nf3', 'e2e4')
        Returns True if valid, False otherwise
        """
        try:
            # Try parsing as SAN (e4, Nf3)
            move = self.board.parse_san(move_str)
        except:
            try:
                # Try parsing as UCI (e2e4)
                move = chess.Move.from_uci(move_str)
                if move not in self.board.legal_moves:
                    return False
            except:
                return False
        
        if move in self.board.legal_moves:
            self.move_history.append(move)
            self.board.push(move)
            return True
        return False
    
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
    
    def undo_move(self):
        """Undo last move"""
        if self.move_history:
            self.board.pop()
            self.move_history.pop()
            return True
        return False
    
    def get_legal_moves(self):
        """Get list of legal moves in SAN notation"""
        return [self.board.san(move) for move in self.board.legal_moves]
    
    def is_checkmate(self):
        """Check if current position is checkmate"""
        return self.board.is_checkmate()
    
    def is_check(self):
        """Check if current position is check"""
        return self.board.is_check()
    
    def is_game_over(self):
        """Check if game is over"""
        return self.board.is_game_over()
    
    def get_fen(self):
        """Get current FEN string"""
        return self.board.fen()
    
    def load_fen(self, fen):
        """Load position from FEN"""
        self.board = chess.Board(fen)
        self.move_history = []
    
    def get_board(self):
        """Get the chess.Board object"""
        return self.board
