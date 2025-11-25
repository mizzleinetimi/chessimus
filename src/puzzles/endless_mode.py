"""Endless puzzle mode - rapid-fire puzzle stream"""

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
from chess_game.renderer import BoardRenderer
from chess_game.input_parser import InputParser

class EndlessMode:
    """Endless puzzle solving mode"""
    
    def __init__(self, config):
        """Initialize endless mode"""
        self.config = config
        self.score = 0
        self.attempts = 0
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
    
    def run(self):
        """Run endless puzzle loop"""
        print("\n🎯 ENDLESS PUZZLE MODE")
        print("Solve puzzles rapidly. Type 'quit' to exit.\n")
        
        while True:
            try:
                # Fetch puzzle
                print("Fetching puzzle...")
                puzzle_json = LichessAPI.get_random_puzzle()
                puzzle_data = PuzzleParser.parse(puzzle_json)
                
                # Solve puzzle
                result = self._solve_puzzle(puzzle_data)
                
                if result == 'quit':
                    break
                elif result == 'solved':
                    self.score += 1
                
                self.attempts += 1
                
                # Show stats
                accuracy = (self.score / self.attempts * 100) if self.attempts > 0 else 0
                print(f"\n📊 Score: {self.score}/{self.attempts} ({accuracy:.1f}%)")
                input("\nPress Enter for next puzzle...")
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"❌ Error: {e}")
                continue
        
        print(f"\n\n🏁 Final Score: {self.score}/{self.attempts}")
        print("Thanks for playing! 👻\n")
    
    def _solve_puzzle(self, puzzle_data):
        """Solve a single puzzle"""
        engine = PuzzleEngine(puzzle_data)
        
        print(f"\n🧩 Puzzle #{puzzle_data['id']}")
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
                if value in ['quit', 'exit']:
                    return 'quit'
                elif value == 'hint':
                    hint = engine.get_hint()
                    print(f"💡 Hint: {hint}")
                    input("Press Enter to continue...")
                    continue
            elif input_type == 'move':
                result, move = engine.check_move(value)
                
                if result == 'correct':
                    print("✅ Correct!")
                elif result == 'complete':
                    print("🎉 Puzzle solved!")
                    return 'solved'
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
        
        return 'solved'
