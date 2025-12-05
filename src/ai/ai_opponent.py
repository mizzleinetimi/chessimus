"""AI Opponent with personality and trash talk"""

import chess
import os
from typing import Dict, Optional
from ai.stockfish_engine import StockfishEngine
from ai.chess_coach import ChessCoach

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIOpponent:
    """AI opponent that plays chess and talks trash"""
    
    DIFFICULTY_DEPTHS = {
        'beginner': 5,
        'intermediate': 10,
        'strong': 15,
        'frankenstein': 18
    }
    
    def __init__(self, difficulty: str = 'intermediate', personality: str = 'spooky'):
        """
        Initialize AI opponent
        
        Args:
            difficulty: 'beginner', 'intermediate', 'strong', 'frankenstein'
            personality: 'spooky', 'normal', 'silent'
        """
        self.difficulty = difficulty
        self.personality = personality
        depth = self.DIFFICULTY_DEPTHS.get(difficulty, 10)
        self.engine = StockfishEngine(depth=depth)
        self.coach = ChessCoach(style='spooky' if personality == 'spooky' else 'normal')
        self.trash_talk_enabled = personality == 'spooky'
        
        # Initialize OpenAI client if available
        self.openai_client = None
        if OPENAI_AVAILABLE and os.getenv('OPENAI_API_KEY'):
            try:
                self.openai_client = OpenAI()
            except:
                pass
    
    def start(self) -> bool:
        """Start the AI opponent"""
        return self.engine.start()
    
    def stop(self):
        """Stop the AI opponent"""
        self.engine.stop()
    
    def get_move(self, board: chess.Board) -> Optional[str]:
        """
        Get AI's move
        
        Returns:
            Move in SAN notation
        """
        return self.engine.get_best_move(board)
    
    def _generate_dynamic_taunt(self, context: str, board: Optional[chess.Board] = None, 
                               move: Optional[str] = None) -> Optional[str]:
        """Generate dynamic trash talk using OpenAI with game context"""
        if not self.openai_client:
            return None
        
        try:
            # Build context with game state
            full_context = context
            if board:
                # Add position info
                full_context += f"\n\nCurrent position: {board.fen()}"
                if board.is_check():
                    full_context += " (King is in check!)"
                
                # Add material count
                material = self._get_material_balance(board)
                if material != 0:
                    full_context += f"\nMaterial balance: {'+' if material > 0 else ''}{material} (positive = AI winning)"
            
            if move:
                full_context += f"\nMove played: {move}"
            
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",  # Fastest model for quick responses
                messages=[
                    {"role": "system", "content": "You are a spooky, Halloween-themed chess AI called Frankenstein. You trash talk in a playful, ghostly way using emojis like 👻 🎃 💀. Keep responses to 1 short sentence (max 15 words). Be creative and funny, not mean. Use the game context to make relevant comments."},
                    {"role": "user", "content": full_context}
                ],
                max_tokens=30,  # Reduced for faster responses
                temperature=0.9,
                timeout=3.0  # 3 second timeout to avoid long waits
            )
            return response.choices[0].message.content.strip()
        except:
            return None
    
    def _get_material_balance(self, board: chess.Board) -> int:
        """Calculate material balance (positive = white/AI ahead)"""
        piece_values = {
            chess.PAWN: 1,
            chess.KNIGHT: 3,
            chess.BISHOP: 3,
            chess.ROOK: 5,
            chess.QUEEN: 9
        }
        
        balance = 0
        for square in chess.SQUARES:
            piece = board.piece_at(square)
            if piece and piece.piece_type != chess.KING:
                value = piece_values[piece.piece_type]
                balance += value if piece.color == chess.BLACK else -value
        
        return balance
    
    def get_opening_taunt(self) -> str:
        """Get opening trash talk"""
        if not self.trash_talk_enabled:
            return ""
        
        # Try dynamic generation first
        dynamic = self._generate_dynamic_taunt("Generate a spooky opening taunt to start a chess game")
        if dynamic:
            return dynamic
        
        # Fallback to static taunts
        taunts = [
            "👻 Prepare to be haunted by my superior moves...",
            "🎃 Your pieces will tremble before the Frankenstein AI!",
            "👻 I've calculated your defeat in 1000 variations...",
            "🎃 Even my worst move is better than your best!",
            "👻 Boo! Did I scare you? Wait until you see my tactics..."
        ]
        import random
        return random.choice(taunts)
    
    def get_move_taunt(self, board_after: chess.Board, my_move: str, 
                       player_last_move: Optional[str] = None) -> str:
        """
        Get trash talk after making a move
        
        Args:
            board_after: Board after AI's move
            my_move: AI's move
            player_last_move: Player's last move (for analysis)
        
        Returns:
            Trash talk message
        """
        if not self.trash_talk_enabled:
            return ""
        
        # Analyze player's last move if provided
        if player_last_move:
            board_before = board_after.copy()
            board_before.pop()  # Undo AI move
            board_before.pop()  # Undo player move
            
            analysis = self.engine.analyze_move(board_before, player_last_move)
            
            if analysis['classification'] == 'blunder':
                return self._get_blunder_taunt(board_after, player_last_move)
            elif analysis['classification'] == 'mistake':
                return self._get_mistake_taunt(board_after, player_last_move)
            elif analysis['classification'] in ['best', 'good']:
                return self._get_good_move_taunt(board_after, player_last_move)
        
        # General taunts
        return self._get_general_taunt(board_after, my_move)
    
    def get_response_to_player_move(self, board: chess.Board, 
                                    player_move: str) -> str:
        """
        React to player's move with trash talk
        
        Args:
            board: Board after player's move
            player_move: Player's move in SAN
        
        Returns:
            Reaction message
        """
        if not self.trash_talk_enabled:
            return ""
        
        # Make a temporary board to analyze
        board_before = board.copy()
        board_before.pop()  # Undo player's move
        
        analysis = self.engine.analyze_move(board_before, player_move)
        
        if analysis['classification'] == 'blunder':
            return self._get_blunder_reaction()
        elif analysis['classification'] == 'mistake':
            return self._get_mistake_reaction()
        elif analysis['classification'] == 'inaccuracy':
            return self._get_inaccuracy_reaction()
        elif analysis['classification'] in ['best', 'good']:
            return self._get_good_move_reaction()
        
        return ""
    
    def get_checkmate_taunt(self, i_won: bool) -> str:
        """Get final taunt for checkmate"""
        if not self.trash_talk_enabled:
            return ""
        
        if i_won:
            taunts = [
                "👻 CHECKMATE! Your king has been SPOOKED into submission!",
                "🎃 Game over! The Frankenstein AI claims another victim!",
                "👻 Boo-hoo! Better luck in the afterlife!",
                "🎃 Your pieces are now haunting the graveyard!",
                "👻 Checkmate! I didn't even need all my processing power..."
            ]
        else:
            taunts = [
                "👻 Impossible! You must have made a deal with the devil!",
                "🎃 Curses! I'll haunt your dreams for this defeat!",
                "👻 This isn't over... I'll be back from the grave!",
                "🎃 You got lucky... the spirits were against me today!",
                "👻 Checkmate... but I let you win to give you false hope!"
            ]
        
        import random
        return random.choice(taunts)
    
    def _get_blunder_taunt(self, board: Optional[chess.Board] = None, 
                          move: Optional[str] = None) -> str:
        """Taunt for player's blunder"""
        dynamic = self._generate_dynamic_taunt(
            "The player just made a terrible blunder in chess. Mock them playfully",
            board, move
        )
        if dynamic:
            return dynamic
        
        taunts = [
            "💥 BLUNDER! Even a ghost could see that was terrible!",
            "👻 Bahahaha! Did you just donate that piece to me?",
            "🎃 That move made my circuits laugh!",
            "👻 I've seen scarier moves in a graveyard!",
            "💀 That blunder will haunt you forever!"
        ]
        import random
        return random.choice(taunts)
    
    def _get_mistake_taunt(self, board: Optional[chess.Board] = None,
                          move: Optional[str] = None) -> str:
        """Taunt for player's mistake"""
        dynamic = self._generate_dynamic_taunt(
            "The player made a mistake in chess. Tease them lightly",
            board, move
        )
        if dynamic:
            return dynamic
        
        taunts = [
            "👻 Ooh, that's a mistake! The spirits are disappointed...",
            "🎃 Not your best move... I expected better!",
            "👻 Tsk tsk... even a zombie could play better!",
            "🎃 That move gave me the chills... of laughter!",
            "👻 Mistake detected! My ghostly senses are tingling!"
        ]
        import random
        return random.choice(taunts)
    
    def _get_good_move_taunt(self, board: Optional[chess.Board] = None,
                            move: Optional[str] = None) -> str:
        """Taunt when player makes a good move"""
        dynamic = self._generate_dynamic_taunt(
            "The player made a good chess move. Acknowledge it but stay confident",
            board, move
        )
        if dynamic:
            return dynamic
        
        taunts = [
            "👻 Hmm, not bad... for a mortal.",
            "🎃 A decent move, but I've already calculated my response!",
            "👻 Impressive... but futile!",
            "🎃 Good move! Too bad it won't save you...",
            "👻 You're learning... but I'm still 10 moves ahead!"
        ]
        import random
        return random.choice(taunts)
    
    def _get_general_taunt(self, board: Optional[chess.Board] = None,
                          move: Optional[str] = None) -> str:
        """General trash talk"""
        dynamic = self._generate_dynamic_taunt(
            "You (the AI) just made a chess move. Say something spooky and confident",
            board, move
        )
        if dynamic:
            return dynamic
        
        taunts = [
            "👻 Behold my superior calculation!",
            "🎃 This move will haunt your position!",
            "👻 Can you feel the ghostly pressure?",
            "🎃 My pieces move like phantoms in the night!",
            "👻 Resistance is futile, mortal!"
        ]
        import random
        return random.choice(taunts)
    
    def _get_blunder_reaction(self) -> str:
        """React to player's blunder"""
        reactions = [
            "💥 WHAT?! Did you just... BAHAHAHA!",
            "👻 *ghostly cackling* That's a BLUNDER!",
            "🎃 Oh my! Even I didn't expect THAT bad!",
            "💀 That piece is MINE now! Mwahahaha!",
            "👻 *spooky laughter* Thank you for the free piece!"
        ]
        import random
        return random.choice(reactions)
    
    def _get_mistake_reaction(self) -> str:
        """React to player's mistake"""
        reactions = [
            "👻 Ooh, that's not good for you...",
            "🎃 I sense weakness in your position!",
            "👻 The spirits whisper... 'mistake'!",
            "🎃 Interesting choice... for me!",
            "👻 My ghostly senses detect an error!"
        ]
        import random
        return random.choice(reactions)
    
    def _get_inaccuracy_reaction(self) -> str:
        """React to player's inaccuracy"""
        reactions = [
            "👻 Hmm, not quite optimal...",
            "🎃 I would have played differently...",
            "👻 The spirits suggest a better move existed!",
            "🎃 Acceptable, but not perfect!",
            "👻 My calculations show a superior alternative!"
        ]
        import random
        return random.choice(reactions)
    
    def _get_good_move_reaction(self) -> str:
        """React to player's good move"""
        reactions = [
            "👻 Hmph! A worthy move...",
            "🎃 Impressive... but I'm not worried!",
            "👻 Good move! But can you keep it up?",
            "🎃 The spirits approve... barely!",
            "👻 Not bad! This might be interesting after all..."
        ]
        import random
        return random.choice(reactions)
