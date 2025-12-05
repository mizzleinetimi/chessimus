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
        self.last_move = None
    
    def run(self):
        """Run play mode"""
        print("\n♟️  PLAY MODE")
        print("Enter moves in algebraic notation (e.g., e4, Nf3)")
        print("Commands: undo, moves, quit\n")
        
        while not self.engine.is_game_over():
            self.renderer.clear_screen()
            
            # Highlight last move
            highlight_squares = []
            from_square = None
            if self.last_move:
                from_square = self.last_move[0]
                highlight_squares = [self.last_move[1]]
            
            print(self.renderer.render(self.engine.get_board(), highlight_squares, from_square))
            
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
                board_before = self.engine.get_board().copy()
                try:
                    move_obj = board_before.parse_san(value)
                    # Store move info for highlighting BEFORE making the move
                    self.last_move = (move_obj.from_square, move_obj.to_square, value)
                except:
                    pass
                
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
            
            # Get initial move for highlighting
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
            
            print(f"Puzzle #{puzzle_data['id']}")
            print(f"Rating: {puzzle_data['rating']}")
            print(f"Themes: {', '.join(puzzle_data['themes'])}\n")
            
            feedback_message = ""
            
            while not engine.is_complete():
                self.renderer.clear_screen()
                
                # Highlight last move
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
                    feedback_message = ""  # Clear after showing
                
                user_input = input("\nYour move (or 'quit', 'hint', 'solution'): ").strip()
                input_type, value = InputParser.parse(user_input)
                
                if input_type == 'command':
                    if value in ['quit', 'exit', 'menu']:
                        break
                    elif value == 'hint':
                        hint = engine.get_hint()
                        print(f"💡 Hint: {hint}")
                        input("Press Enter to continue...")
                    elif value == 'solution':
                        solution = engine.get_solution_str()
                        print(f"🔑 Solution: {solution}")
                        input("Press Enter to continue...")
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
                        
                        self.renderer.clear_screen()
                        if last_move:
                            print(self.renderer.render(engine.get_board(), [last_move[1]], last_move[0]))
                        else:
                            print(self.renderer.render(engine.get_board()))
                        print("✅ Correct! Continue...")
                        input("Press Enter...")
                    elif result == 'complete':
                        self.renderer.clear_screen()
                        if opponent_san:
                            # If there was a final opponent move (unlikely for complete, but possible if puzzle ends on opponent move)
                            # Actually check_move returns opponent_san if it made a move.
                            board_after = engine.get_board()
                            opponent_move_obj = board_after.move_stack[-1]
                            last_move = (opponent_move_obj.from_square, opponent_move_obj.to_square, opponent_san)
                        
                        if last_move:
                            print(self.renderer.render(engine.get_board(), [last_move[1]], last_move[0]))
                        else:
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
                        else:
                            feedback_message = f"❌ Invalid move: {move}"
        
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
            print(f"5. Highlight moves: {self.config.get('highlight_moves', True)}")
            print(f"6. Coach style: {self.config.get('coach_style', 'normal')}")
            print(f"7. Show explanations: {self.config.get('show_explanations', True)}")
            print("8. Back to menu")
            
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
                self.config.toggle('highlight_moves')
                self.config.save()
            elif choice == '6':
                self._change_coach_style()
            elif choice == '7':
                self.config.toggle('show_explanations')
                self.config.save()
            elif choice == '8':
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
