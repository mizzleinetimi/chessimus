"""LLM-powered chess coach using OpenAI"""

import os
from typing import Dict, Optional
from openai import OpenAI
import chess


class ChessCoach:
    """AI chess coach that explains moves and provides teaching"""
    
    def __init__(self, api_key: Optional[str] = None, model: str = "gpt-4o-mini", style: str = "normal"):
        """
        Initialize chess coach
        
        Args:
            api_key: OpenAI API key (or uses OPENAI_API_KEY env var)
            model: OpenAI model to use
            style: Coaching style ('normal', 'spooky', 'beginner', 'advanced')
        """
        self.api_key = api_key or os.getenv('OPENAI_API_KEY')
        self.model = model
        self.style = style
        self.client = OpenAI(api_key=self.api_key) if self.api_key else None
    
    def explain_position(self, board: chess.Board, eval_data: Dict) -> str:
        """
        Explain the current position
        
        Args:
            board: Current board state
            eval_data: Stockfish evaluation data
        
        Returns:
            Human-friendly explanation
        """
        if not self.client:
            return "⚠️  OpenAI API key not set. Set OPENAI_API_KEY environment variable."
        
        prompt = self._build_position_prompt(board, eval_data)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️  Coach error: {str(e)}"
    
    def explain_move(self, board_before: chess.Board, move_san: str, 
                     analysis: Dict, eval_before: Dict) -> str:
        """
        Explain why a move is good or bad
        
        Args:
            board_before: Board state before move
            move_san: Move in SAN notation
            analysis: Move analysis from Stockfish
            eval_before: Position evaluation before move
        
        Returns:
            Explanation of the move
        """
        if not self.client:
            return "⚠️  OpenAI API key not set."
        
        prompt = self._build_move_explanation_prompt(board_before, move_san, analysis, eval_before)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=150,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️  Coach error: {str(e)}"
    
    def explain_tactic(self, board: chess.Board, best_move: str, 
                       top_moves: list) -> str:
        """
        Explain tactical ideas in the position
        
        Args:
            board: Current board state
            best_move: Best move from engine
            top_moves: List of top moves with scores
        
        Returns:
            Tactical explanation
        """
        if not self.client:
            return "⚠️  OpenAI API key not set."
        
        prompt = self._build_tactic_prompt(board, best_move, top_moves)
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=200,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️  Coach error: {str(e)}"
    
    def explain_puzzle(self, puzzle_data: Dict) -> str:
        """
        Explain a puzzle's theme and what to look for
        
        Args:
            puzzle_data: Puzzle information
        
        Returns:
            Puzzle explanation
        """
        if not self.client:
            return "⚠️  OpenAI API key not set."
        
        themes = ', '.join(puzzle_data.get('themes', []))
        rating = puzzle_data.get('rating', 'unknown')
        
        prompt = f"""Explain this chess puzzle briefly:
Rating: {rating}
Themes: {themes}

Give a 1-2 sentence hint about what tactical pattern to look for, without giving away the solution."""
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": self._get_system_prompt()},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=100,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            return f"⚠️  Coach error: {str(e)}"
    
    def _get_system_prompt(self) -> str:
        """Get system prompt based on coaching style"""
        base = "You are a helpful chess coach. Be concise and clear."
        
        if self.style == 'spooky':
            return base + " Add a subtle spooky/ghostly tone to your explanations. Use occasional ghost emoji 👻."
        elif self.style == 'beginner':
            return base + " Explain concepts simply for beginners. Avoid complex terminology."
        elif self.style == 'advanced':
            return base + " Use precise chess terminology. Be analytical and detailed."
        else:
            return base + " Explain in a friendly, accessible way."
    
    def _build_position_prompt(self, board: chess.Board, eval_data: Dict) -> str:
        """Build prompt for position explanation"""
        fen = board.fen()
        score = eval_data.get('score', 0)
        best_move = eval_data.get('best_move', 'unknown')
        
        return f"""Analyze this chess position briefly:
FEN: {fen}
Evaluation: {score:+.2f} (positive = white advantage)
Best move: {best_move}
Turn: {'White' if board.turn else 'Black'}

In 2-3 sentences, explain:
1. Who is better and why
2. What the key idea or plan is"""
    
    def _build_move_explanation_prompt(self, board: chess.Board, move_san: str,
                                      analysis: Dict, eval_before: Dict) -> str:
        """Build prompt for move explanation"""
        classification = analysis.get('classification', 'unknown')
        eval_change = analysis.get('eval_change', 0)
        best_move = analysis.get('best_move', 'unknown')
        
        if classification in ['best', 'good']:
            return f"""The player just played {move_san}, which is a {classification} move.
Evaluation change: {eval_change:+.2f}

In 1-2 sentences, briefly explain why this move is good."""
        else:
            return f"""The player just played {move_san}, which is a {classification}.
Evaluation change: {eval_change:+.2f}
Better move was: {best_move}

In 2 sentences, explain:
1. Why the played move is problematic
2. Why the better move is superior"""
    
    def _build_tactic_prompt(self, board: chess.Board, best_move: str,
                            top_moves: list) -> str:
        """Build prompt for tactical explanation"""
        fen = board.fen()
        moves_str = ', '.join([f"{move} ({score:+.2f})" for move, score in top_moves[:3]])
        
        return f"""Explain the key tactical idea in this position:
FEN: {fen}
Best move: {best_move}
Top moves: {moves_str}

In 2-3 sentences, explain what tactical pattern or strategic idea is present."""
