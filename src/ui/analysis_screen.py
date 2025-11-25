"""Analysis mode screen with Stockfish integration"""

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from chess_game.input_parser import InputParser
from ai.stockfish_engine import StockfishEngine


class AnalysisScreen:
    """Analysis mode with engine evaluation"""
    
    def __init__(self, config):
        self.config = config
        self.engine = ChessEngine()
        self.stockfish = StockfishEngine(depth=15)
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
    
    def run(self):
        """Run analysis mode"""
        print("\n🤖 ANALYSIS MODE")
        print("Play moves and get engine analysis!")
        print("Commands: best, eval, top3, undo, quit\n")
        
        # Start Stockfish
        if not self.stockfish.start():
            print("❌ Stockfish engine not found!")
            print("Install with: brew install stockfish")
            input("\nPress Enter to return to menu...")
            return
        
        print("✅ Stockfish engine ready!\n")
        
        try:
            while not self.engine.is_game_over():
                self.renderer.clear_screen()
                print(self.renderer.render(self.engine.get_board()))
                
                # Show evaluation
                eval_data = self.stockfish.get_evaluation(self.engine.get_board())
                print(f"\n📊 Evaluation: {eval_data['evaluation_text']} ({eval_data['score']:+.2f})")
                print(f"💡 Best move: {eval_data['best_move']}")
                
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
                    elif value == 'best':
                        best = self.stockfish.get_best_move(self.engine.get_board())
                        print(f"💡 Best move: {best}")
                        input("Press Enter to continue...")
                    elif value == 'eval':
                        eval_data = self.stockfish.get_evaluation(self.engine.get_board())
                        print(f"\n📊 Detailed Evaluation:")
                        print(f"   Score: {eval_data['score']:+.2f}")
                        print(f"   Assessment: {eval_data['evaluation_text']}")
                        print(f"   Best move: {eval_data['best_move']}")
                        if eval_data['mate']:
                            print(f"   Mate in: {eval_data['mate']}")
                        input("\nPress Enter to continue...")
                    elif value == 'top3':
                        top_moves = self.stockfish.get_top_moves(self.engine.get_board(), 3)
                        print(f"\n🎯 Top 3 Moves:")
                        for i, (move, score) in enumerate(top_moves, 1):
                            print(f"   {i}. {move} ({score:+.2f})")
                        input("\nPress Enter to continue...")
                    elif value == 'moves':
                        moves = self.engine.get_legal_moves()
                        print(f"Legal moves: {', '.join(moves[:20])}")
                        if len(moves) > 20:
                            print(f"... and {len(moves) - 20} more")
                        input("\nPress Enter to continue...")
                
                elif input_type == 'move':
                    # Analyze the move before making it
                    board_before = self.engine.get_board().copy()
                    
                    if self.engine.make_move(value):
                        # Analyze move quality
                        analysis = self.stockfish.analyze_move(board_before, value)
                        
                        # Show feedback
                        if analysis['classification'] == 'best':
                            print("✅ Best move!")
                        elif analysis['classification'] == 'good':
                            print("✅ Good move!")
                        elif analysis['classification'] == 'inaccuracy':
                            print("⚠️  Inaccuracy")
                            print(f"   Better: {analysis['best_move']}")
                        elif analysis['classification'] == 'mistake':
                            print("❌ Mistake!")
                            print(f"   Better: {analysis['best_move']}")
                            print(f"   Lost: {-analysis['eval_change']:.2f} pawns")
                        elif analysis['classification'] == 'blunder':
                            print("💥 BLUNDER!")
                            print(f"   Better: {analysis['best_move']}")
                            print(f"   Lost: {-analysis['eval_change']:.2f} pawns")
                        
                        input("Press Enter to continue...")
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
            # Always stop the engine
            self.stockfish.stop()
            print("\n✅ Engine stopped")
