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
        
        # Get the initial position's last move (the move that led to this puzzle position)
        board = engine.get_board()
        last_move = None
        
        # Use the last move from parser if available
        if puzzle_data.get('last_move_uci'):
            try:
                uci = puzzle_data['last_move_uci']
                move = chess.Move.from_uci(uci)
                last_move = (move.from_square, move.to_square, puzzle_data.get('last_move_san', uci))
            except:
                pass
        elif len(board.move_stack) > 0:
            initial_move = board.move_stack[-1]
            last_move = (initial_move.from_square, initial_move.to_square, board.san(initial_move))
        
        print(f"\n🧩 Puzzle #{puzzle_data['id']}")
        print(f"Rating: {puzzle_data['rating']}")
        print(f"Themes: {', '.join(puzzle_data['themes'])}\n")
        
        feedback_message = ""
        
        while not engine.is_complete():
            self.renderer.clear_screen()
            
            # Highlight last move (always enabled for puzzles)
            highlight_squares = []
            from_square = None
            if last_move and isinstance(last_move, tuple) and len(last_move) == 3:
                from_square = last_move[0]
                highlight_squares = [last_move[1]]
            
            print(self.renderer.render(engine.get_board(), highlight_squares, from_square))
            
            # Show whose turn it is
            turn = engine.get_turn_info()
            print(f"🎯 {turn} to play and win!")
            
            if feedback_message:
                print(f"\n{feedback_message}")
                feedback_message = ""
            
            print("\n💡 Commands: hint, solution, help, quit")
            user_input = input("Your move: ").strip()
            
            input_type, value = InputParser.parse(user_input)
            
            if input_type == 'command':
                if value in ['quit', 'exit']:
                    return 'quit'
                elif value == 'help':
                    print("\n📋 Available Commands:")
                    print("   hint     - Get a hint for the puzzle")
                    print("   solution - Show the full solution")
                    print("   quit     - Return to main menu")
                    print("\n📍 Square Query: Type a square (e.g., 'e4') to see possible moves")
                    input("\nPress Enter to continue...")
                    continue
                elif value == 'hint':
                    hint = engine.get_hint()
                    print(f"💡 Hint: {hint}")
                    input("Press Enter to continue...")
                    continue
                elif value == 'solution':
                    solution = engine.get_solution_str()
                    print(f"🔑 Solution: {solution}")
                    input("Press Enter to continue...")
                    continue
            elif input_type == 'move':
                # Get move object before checking
                board_copy = engine.get_board().copy()
                try:
                    move_obj = board_copy.parse_san(value)
                    from_sq = move_obj.from_square
                    to_sq = move_obj.to_square
                    last_move = (from_sq, to_sq, value)
                except:
                    last_move = None
                
                result, move, opponent_san = engine.check_move(value)
                
                if result == 'correct':
                    # Get opponent's move that was just made
                    board_after = engine.get_board()
                    if opponent_san:
                        opponent_move_obj = board_after.move_stack[-1]
                        last_move = (opponent_move_obj.from_square, opponent_move_obj.to_square, opponent_san)
                    
                    # Show the move on the board
                    self.renderer.clear_screen()
                    if last_move:
                        print(self.renderer.render(engine.get_board(), [last_move[1]], last_move[0]))
                    else:
                        print(self.renderer.render(engine.get_board()))
                    print("✅ Correct!")
                    input("Press Enter to continue...")
                elif result == 'complete':
                    self.renderer.clear_screen()
                    if opponent_san:
                        board_after = engine.get_board()
                        opponent_move_obj = board_after.move_stack[-1]
                        last_move = (opponent_move_obj.from_square, opponent_move_obj.to_square, opponent_san)
                        
                    if last_move:
                        print(self.renderer.render(engine.get_board(), [last_move[1]], last_move[0]))
                    else:
                        print(self.renderer.render(engine.get_board()))
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
                        feedback_message = "❌ Incorrect. Try again!"
                        last_move = None  # Clear highlight on wrong move
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
                        print(f"📍 Moves from {value}: {', '.join(moves)}")
                        input("Press Enter to continue...")
                    else:
                        feedback_message = f"❌ Invalid move: {move}"
        
        return 'solved'
