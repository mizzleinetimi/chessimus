"""Game screens for different modes"""

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from chess_game.input_parser import InputParser
from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine

class PlayScreen:
    """Free play mode screen"""
    
    def __init__(self, config):
        self.config = config
        self.engine = ChessEngine()
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
    
    def run(self):
        """Run play mode"""
        print("\n♟️  PLAY MODE")
        print("Enter moves in algebraic notation (e.g., e4, Nf3)")
        print("Commands: undo, moves, quit\n")
        
        while not self.engine.is_game_over():
            self.renderer.clear_screen()
            print(self.renderer.render(self.engine.get_board()))
            
            if self.engine.is_check():
                print("⚠️  Check!")
            
            user_input = input("\nYour move: ").strip()
            input_type, value = InputParser.parse(user_input)
            
            if input_type == 'command':
                if value in ['quit', 'exit', 'menu']:
                    break
                elif value == 'undo':
                    if self.engine.undo_move():
                        print("↩️  Move undone")
                    else:
                        print("❌ No moves to undo")
                elif value == 'moves':
                    moves = self.engine.get_legal_moves()
                    print(f"Legal moves: {', '.join(moves[:20])}")
                    if len(moves) > 20:
                        print(f"... and {len(moves) - 20} more")
                    input("\nPress Enter to continue...")
            elif input_type == 'move':
                # Try to make the move
                if self.engine.make_move(value):
                    print("✅ Move made")
                else:
                    # If move fails, check if it's a square query
                    moves, dest_squares = self.engine.get_moves_from_square(value)
                    if moves:
                        self.renderer.clear_screen()
                        print(self.renderer.render(self.engine.get_board(), dest_squares))
                        print(f"📍 Moves from {value}: {', '.join(moves)}")
                        input("Press Enter to continue...")
                    else:
                        print("❌ Illegal move")
                        input("Press Enter to continue...")
        
        if self.engine.is_checkmate():
            print("\n🎉 Checkmate!")
        elif self.engine.is_game_over():
            print("\n🤝 Game over!")

class PuzzleScreen:
    """Single puzzle mode screen"""
    
    def __init__(self, config):
        self.config = config
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
    
    def run(self):
        """Run puzzle mode"""
        print("\n🧩 PUZZLE MODE")
        print("Fetching puzzle from Lichess...\n")
        
        try:
            puzzle_json = LichessAPI.get_random_puzzle()
            puzzle_data = PuzzleParser.parse(puzzle_json)
            engine = PuzzleEngine(puzzle_data)
            
            print(f"Puzzle #{puzzle_data['id']}")
            print(f"Rating: {puzzle_data['rating']}")
            print(f"Themes: {', '.join(puzzle_data['themes'])}\n")
            
            while not engine.is_complete():
                self.renderer.clear_screen()
                print(self.renderer.render(engine.get_board()))
                
                # Show whose turn it is
                turn = engine.get_turn_info()
                print(f"🎯 {turn} to play and win!")
                
                user_input = input("\nYour move (or 'quit', 'hint'): ").strip()
                input_type, value = InputParser.parse(user_input)
                
                if input_type == 'command':
                    if value in ['quit', 'exit', 'menu']:
                        break
                    elif value == 'hint':
                        hint = engine.get_hint()
                        print(f"💡 Hint: {hint}")
                        input("Press Enter to continue...")
                elif input_type == 'move':
                    result, move = engine.check_move(value)
                    
                    if result == 'correct':
                        print("✅ Correct! Continue...")
                        input("Press Enter...")
                    elif result == 'complete':
                        self.renderer.clear_screen()
                        print(self.renderer.render(engine.get_board()))
                        print("\n🎉 Puzzle solved!")
                        input("\nPress Enter to return to menu...")
                        break
                    elif result == 'incorrect':
                        # Check if it's a square query
                        moves, dest_squares = engine.get_moves_from_square(value)
                        if moves:
                            self.renderer.clear_screen()
                            print(self.renderer.render(engine.get_board(), dest_squares))
                            turn = engine.get_turn_info()
                            print(f"🎯 {turn} to play and win!")
                            print(f"📍 Moves from {value}: {', '.join(moves)}")
                            input("Press Enter to continue...")
                        else:
                            print("❌ Incorrect. Try again!")
                            input("Press Enter to continue...")
                    elif result == 'error':
                        # Check if it's a square query
                        moves, dest_squares = engine.get_moves_from_square(value)
                        if moves:
                            self.renderer.clear_screen()
                            print(self.renderer.render(engine.get_board(), dest_squares))
                            turn = engine.get_turn_info()
                            print(f"🎯 {turn} to play and win!")
                            print(f"📍 Moves from {value}: {', '.join(moves)}")
                            input("Press Enter to continue...")
                        else:
                            print(f"❌ Invalid move: {move}")
                            input("Press Enter to continue...")
        
        except Exception as e:
            print(f"❌ Error: {e}")
            input("\nPress Enter to return to menu...")

class SettingsScreen:
    """Settings configuration screen"""
    
    def __init__(self, config):
        self.config = config
    
    def run(self):
        """Run settings screen"""
        while True:
            print("\n" + "="*40)
            print("⚙️  SETTINGS")
            print("="*40)
            print(f"\n1. Theme: {self.config.get('theme', 'default')}")
            print(f"2. Unicode pieces: {self.config.get('use_unicode', True)}")
            print(f"3. Large board: {self.config.get('large_board', True)}")
            print(f"4. Animations: {self.config.get('animations', True)}")
            print(f"5. Coach style: {self.config.get('coach_style', 'normal')}")
            print(f"6. Show explanations: {self.config.get('show_explanations', True)}")
            print("7. Back to menu")
            
            choice = input("\nSelect option: ").strip()
            
            if choice == '1':
                self._change_theme()
            elif choice == '2':
                self.config.toggle('use_unicode')
                self.config.save()
            elif choice == '3':
                self.config.toggle('large_board')
                self.config.save()
            elif choice == '4':
                self.config.toggle('animations')
                self.config.save()
            elif choice == '5':
                self._change_coach_style()
            elif choice == '6':
                self.config.toggle('show_explanations')
                self.config.save()
            elif choice == '7':
                break
    
    def _change_theme(self):
        """Change theme"""
        print("\nAvailable themes:")
        print("1. default")
        print("2. spooky 👻")
        
        choice = input("Select theme: ").strip()
        if choice == '1':
            self.config.set('theme', 'default')
        elif choice == '2':
            self.config.set('theme', 'spooky')
        
        self.config.save()
    
    def _change_coach_style(self):
        """Change coaching style"""
        print("\nCoaching styles:")
        print("1. normal - Friendly and accessible")
        print("2. beginner - Simple explanations")
        print("3. advanced - Detailed analysis")
        print("4. spooky 👻 - Ghostly coaching")
        
        choice = input("Select style: ").strip()
        if choice == '1':
            self.config.set('coach_style', 'normal')
        elif choice == '2':
            self.config.set('coach_style', 'beginner')
        elif choice == '3':
            self.config.set('coach_style', 'advanced')
        elif choice == '4':
            self.config.set('coach_style', 'spooky')
        
        self.config.save()
