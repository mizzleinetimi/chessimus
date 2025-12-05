"""Stockfish chess engine integration"""

import chess
import chess.engine
from typing import Optional, Dict, List, Tuple


class StockfishEngine:
    """Wrapper for Stockfish chess engine"""
    
    def __init__(self, stockfish_path: str = "stockfish", depth: int = 15):
        """
        Initialize Stockfish engine
        
        Args:
            stockfish_path: Path to stockfish binary
            depth: Search depth (higher = stronger but slower)
        """
        self.stockfish_path = stockfish_path
        self.depth = depth
        self.engine: Optional[chess.engine.SimpleEngine] = None
    
    def start(self):
        """Start the engine"""
        try:
            self.engine = chess.engine.SimpleEngine.popen_uci(self.stockfish_path)
            return True
        except Exception as e:
            print(f"Failed to start Stockfish: {e}")
            return False
    
    def stop(self):
        """Stop the engine"""
        if self.engine:
            self.engine.quit()
            self.engine = None
    
    def get_best_move(self, board: chess.Board) -> Optional[str]:
        """
        Get best move for current position
        
        Returns:
            Best move in SAN notation, or None if engine not running
        """
        if not self.engine:
            return None
        
        try:
            result = self.engine.play(board, chess.engine.Limit(depth=self.depth, time=5.0))
            return board.san(result.move)
        except Exception as e:
            print(f"Stockfish error: {e}")
            return None
    
    def get_evaluation(self, board: chess.Board) -> Dict:
        """
        Get position evaluation
        
        Returns:
            {
                'score': float (in pawns, positive = white advantage),
                'mate': int or None (moves to mate),
                'best_move': str (SAN notation),
                'evaluation_text': str (human readable)
            }
        """
        if not self.engine:
            return {
                'score': 0.0,
                'mate': None,
                'best_move': None,
                'evaluation_text': 'Engine not running'
            }
        
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth, time=3.0))
            score = info['score'].relative
            
            # Extract score
            if score.is_mate():
                mate_in = score.mate()
                score_value = 100.0 if mate_in > 0 else -100.0
                eval_text = f"Mate in {abs(mate_in)}"
            else:
                score_value = score.score() / 100.0  # Convert centipawns to pawns
                eval_text = self._score_to_text(score_value)
            
            # Get best move
            best_move = None
            if 'pv' in info and info['pv']:
                best_move = board.san(info['pv'][0])
            
            return {
                'score': score_value,
                'mate': score.mate() if score.is_mate() else None,
                'best_move': best_move,
                'evaluation_text': eval_text
            }
        except Exception as e:
            return {
                'score': 0.0,
                'mate': None,
                'best_move': None,
                'evaluation_text': f'Error: {e}'
            }
    
    def analyze_move(self, board_before: chess.Board, move_san: str) -> Dict:
        """
        Analyze a move and determine if it's good, bad, or blunder
        
        Returns:
            {
                'classification': str ('best', 'good', 'inaccuracy', 'mistake', 'blunder'),
                'eval_before': float,
                'eval_after': float,
                'eval_change': float,
                'best_move': str
            }
        """
        if not self.engine:
            return {'classification': 'unknown', 'eval_before': 0, 'eval_after': 0, 'eval_change': 0, 'best_move': None}
        
        # Get evaluation before move
        eval_before = self.get_evaluation(board_before)
        
        # Make the move
        board_after = board_before.copy()
        try:
            move = board_before.parse_san(move_san)
            board_after.push(move)
        except:
            return {'classification': 'illegal', 'eval_before': 0, 'eval_after': 0, 'eval_change': 0, 'best_move': None}
        
        # Get evaluation after move
        eval_after = self.get_evaluation(board_after)
        
        # Calculate change (from perspective of player who moved)
        score_before = eval_before['score'] if board_before.turn else -eval_before['score']
        score_after = -eval_after['score'] if board_after.turn else eval_after['score']
        eval_change = score_after - score_before
        
        # Classify move
        classification = self._classify_move(eval_change, move_san == eval_before['best_move'])
        
        return {
            'classification': classification,
            'eval_before': eval_before['score'],
            'eval_after': eval_after['score'],
            'eval_change': eval_change,
            'best_move': eval_before['best_move']
        }
    
    def _classify_move(self, eval_change: float, is_best: bool) -> str:
        """Classify move quality based on evaluation change"""
        if is_best:
            return 'best'
        elif eval_change >= -0.1:
            return 'good'
        elif eval_change >= -0.5:
            return 'inaccuracy'
        elif eval_change >= -1.5:
            return 'mistake'
        else:
            return 'blunder'
    
    def _score_to_text(self, score: float) -> str:
        """Convert numerical score to human-readable text"""
        if score > 3.0:
            return "White is winning"
        elif score > 1.0:
            return "White is better"
        elif score > 0.3:
            return "White is slightly better"
        elif score > -0.3:
            return "Equal position"
        elif score > -1.0:
            return "Black is slightly better"
        elif score > -3.0:
            return "Black is better"
        else:
            return "Black is winning"
    
    def get_top_moves(self, board: chess.Board, num_moves: int = 3) -> List[Tuple[str, float]]:
        """
        Get top N moves with their evaluations
        
        Returns:
            List of (move_san, score) tuples
        """
        if not self.engine:
            return []
        
        try:
            info = self.engine.analyse(board, chess.engine.Limit(depth=self.depth, time=3.0), multipv=num_moves)
            
            moves = []
            for pv_info in info:
                if 'pv' in pv_info and pv_info['pv']:
                    move = board.san(pv_info['pv'][0])
                    score = pv_info['score'].relative
                    score_value = score.score() / 100.0 if not score.is_mate() else (100.0 if score.mate() > 0 else -100.0)
                    moves.append((move, score_value))
            
            return moves
        except:
            return []
