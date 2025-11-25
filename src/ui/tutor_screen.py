"""Tutor Mode - Interactive teaching with AI coach"""

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from chess_game.input_parser import InputParser
from ai.stockfish_engine import StockfishEngine
from ai.chess_coach import ChessCoach


class TutorScreen:
    """Tutor mode with AI coaching"""
    
    def __init__(self, config):
        self.config = config
        self.engine = ChessEngine()
        self.stockfish = StockfishEngine(depth=15)
        self.coach = ChessCoach(style=config.get('coach_style', 'normal'))
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
        self.show_explanations = config.get('show_explanations', True)
    
    def run(self):
        """Run tutor mode"""
        print("\n🧙 TUTOR MODE")
        print("Learn chess with AI coaching!")
        print("Commands: explain, hint, best, undo, quit\n")
        
        # Start engines
        if not self.stockfish.start():
            print("❌ Stockfish engine not found!")
            input("\nPress Enter to return to menu...")
            return
        
        print("✅ AI Tutor ready!\n")
        
        try:
            while not self.engine.is_game_over():
                self.renderer.clear_screen()
                print(self.renderer.render(self.engine.get_board()))
                
                # Show evaluation
                eval_data = self.stockfish.get_evaluation(self.engine.get_board())
                print(f"\n📊 {eval_data['evaluation_text']} ({eval_data['score']:+.2f})")
                
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
                        input("Press Enter to continue...")
                    elif value == 'hint':
                        print(f"\n💡 Best move: {eval_data['best_move']}")
                        input("Press Enter to continue...")
                    elif value == 'best':
                        print(f"\n💡 Best move: {eval_data['best_move']}")
                        # Get top moves
                        top_moves = self.stockfish.get_top_moves(self.engine.get_board(), 3)
                        print("\n🎯 Top 3 moves:")
                        for i, (move, score) in enumerate(top_moves, 1):
                            print(f"   {i}. {move} ({score:+.2f})")
                        input("\nPress Enter to continue...")
                    elif value == 'explain':
                        print("\n🧙 Analyzing position...")
                        explanation = self.coach.explain_position(
                            self.engine.get_board(), 
                            eval_data
                        )
                        print(f"\n{explanation}")
                        input("\nPress Enter to continue...")
                
                elif input_type == 'move':
                    # Store board state before move
                    board_before = self.engine.get_board().copy()
                    eval_before = eval_data
                    
                    if self.engine.make_move(value):
                        # Analyze the move
                        analysis = self.stockfish.analyze_move(board_before, value)
                        
                        # Show immediate feedback
                        if analysis['classification'] == 'best':
                            print("✅ Excellent! Best move!")
                        elif analysis['classification'] == 'good':
                            print("✅ Good move!")
                        elif analysis['classification'] == 'inaccuracy':
                            print("⚠️  Inaccuracy")
                        elif analysis['classification'] == 'mistake':
                            print("❌ Mistake!")
                        elif analysis['classification'] == 'blunder':
                            print("💥 BLUNDER!")
                        
                        # Get AI explanation if enabled
                        if self.show_explanations and analysis['classification'] != 'best':
                            print("\n🧙 Coach is analyzing...")
                            explanation = self.coach.explain_move(
                                board_before, 
                                value, 
                                analysis, 
                                eval_before
                            )
                            print(f"\n{explanation}")
                        
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
                            input("Press Enter to continue...")
            
            if self.engine.is_checkmate():
                print("\n🎉 Checkmate!")
            elif self.engine.is_game_over():
                print("\n🤝 Game over!")
        
        finally:
            self.stockfish.stop()
            print("\n✅ Tutor session ended")
