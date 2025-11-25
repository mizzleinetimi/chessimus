"""Play against AI opponent with trash talk"""

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from chess_game.input_parser import InputParser
from ai.ai_opponent import AIOpponent
import time


class AIOpponentScreen:
    """Play against AI opponent"""
    
    def __init__(self, config):
        self.config = config
        self.engine = ChessEngine()
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
    
    def run(self):
        """Run AI opponent mode"""
        print("\n🤖 AI OPPONENT MODE")
        print("Play against the Frankenstein AI!\n")
        
        # Select difficulty
        print("Select difficulty:")
        print("1. Beginner 🟢")
        print("2. Intermediate 🟡")
        print("3. Strong 🔴")
        print("4. Frankenstein 👻💀 (MAXIMUM SPOOKINESS)")
        
        choice = input("\nDifficulty: ").strip()
        difficulty_map = {
            '1': 'beginner',
            '2': 'intermediate',
            '3': 'strong',
            '4': 'frankenstein'
        }
        difficulty = difficulty_map.get(choice, 'intermediate')
        
        # Initialize AI
        ai = AIOpponent(difficulty=difficulty, personality='spooky')
        if not ai.start():
            print("❌ AI engine not available!")
            input("\nPress Enter to return to menu...")
            return
        
        print(f"\n✅ AI ready at {difficulty} difficulty!")
        
        # Opening taunt
        taunt = ai.get_opening_taunt()
        if taunt:
            print(f"\n{taunt}")
        
        input("\nPress Enter to start...")
        
        try:
            player_last_move = None
            
            while not self.engine.is_game_over():
                self.renderer.clear_screen()
                print(self.renderer.render(self.engine.get_board()))
                
                if self.engine.is_check():
                    if self.engine.get_board().turn:  # White's turn (player)
                        print("⚠️  You're in check!")
                    else:
                        print("👻 Boo! I put you in check!")
                
                # Player's turn
                user_input = input("\nYour move: ").strip()
                input_type, value = InputParser.parse(user_input)
                
                if input_type == 'command':
                    if value in ['quit', 'exit', 'menu']:
                        break
                    elif value == 'undo':
                        # Undo both player and AI moves
                        if self.engine.undo_move() and self.engine.undo_move():
                            print("↩️  Moves undone")
                            player_last_move = None
                        else:
                            print("❌ No moves to undo")
                        input("Press Enter to continue...")
                    elif value == 'hint':
                        print("👻 No hints! Figure it out yourself, mortal!")
                        input("Press Enter to continue...")
                
                elif input_type == 'move':
                    if self.engine.make_move(value):
                        player_last_move = value
                        
                        # AI reacts to player's move
                        reaction = ai.get_response_to_player_move(
                            self.engine.get_board(), 
                            value
                        )
                        if reaction:
                            print(f"\n{reaction}")
                            time.sleep(1.5)
                        
                        # Check if game over after player move
                        if self.engine.is_game_over():
                            break
                        
                        # AI's turn
                        print("\n🤖 AI is thinking...")
                        time.sleep(0.8)  # Dramatic pause
                        
                        ai_move = ai.get_move(self.engine.get_board())
                        if ai_move:
                            self.engine.make_move(ai_move)
                            
                            # AI trash talks
                            taunt = ai.get_move_taunt(
                                self.engine.get_board(),
                                ai_move,
                                player_last_move
                            )
                            
                            print(f"🤖 AI plays: {ai_move}")
                            if taunt:
                                print(f"{taunt}")
                            
                            input("\nPress Enter to continue...")
                    else:
                        # Check if it's a square query
                        moves, dest_squares = self.engine.get_moves_from_square(value)
                        if moves:
                            self.renderer.clear_screen()
                            print(self.renderer.render(self.engine.get_board(), dest_squares))
                            print(f"📍 Moves from {value}: {', '.join(moves)}")
                            input("Press Enter to continue...")
                        else:
                            print("❌ Illegal move")
                            print("👻 Can't even make a legal move? Pathetic!")
                            input("Press Enter to continue...")
            
            # Game over
            self.renderer.clear_screen()
            print(self.renderer.render(self.engine.get_board()))
            
            if self.engine.is_checkmate():
                # Determine winner
                if self.engine.get_board().turn:  # White to move = Black won
                    print("\n🎉 CHECKMATE! You won!")
                    taunt = ai.get_checkmate_taunt(i_won=False)
                else:  # Black to move = White won
                    print("\n💀 CHECKMATE! AI wins!")
                    taunt = ai.get_checkmate_taunt(i_won=True)
                
                if taunt:
                    print(f"\n{taunt}")
            elif self.engine.is_game_over():
                print("\n🤝 Game over - Draw!")
                print("👻 I'll accept this draw... for now!")
        
        finally:
            ai.stop()
            input("\nPress Enter to return to menu...")
