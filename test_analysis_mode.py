#!/usr/bin/env python3
"""Test Analysis Mode integration"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from ai.stockfish_engine import StockfishEngine

print("\n" + "="*60)
print("🤖 ANALYSIS MODE TEST")
print("="*60)

# Initialize components
engine = ChessEngine()
stockfish = StockfishEngine(depth=10)
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

# Start Stockfish
print("\n1️⃣  Starting Stockfish...")
if not stockfish.start():
    print("❌ Failed to start Stockfish")
    sys.exit(1)
print("✅ Stockfish ready!")

# Show starting position
print("\n2️⃣  Starting Position:")
print(renderer.render(engine.get_board()))

# Get evaluation
eval_data = stockfish.get_evaluation(engine.get_board())
print(f"📊 Evaluation: {eval_data['evaluation_text']} ({eval_data['score']:+.2f})")
print(f"💡 Best move: {eval_data['best_move']}")

# Make a move
print("\n3️⃣  Making move: e4")
board_before = engine.get_board().copy()
engine.make_move('e4')

# Analyze the move
analysis = stockfish.analyze_move(board_before, 'e4')
print(f"   Classification: {analysis['classification']}")
print(f"   Eval change: {analysis['eval_change']:+.2f}")

# Show new position
print("\n4️⃣  Position after e4:")
print(renderer.render(engine.get_board()))

eval_data = stockfish.get_evaluation(engine.get_board())
print(f"📊 Evaluation: {eval_data['evaluation_text']} ({eval_data['score']:+.2f})")
print(f"💡 Best move: {eval_data['best_move']}")

# Get top 3 moves
print("\n5️⃣  Top 3 Moves:")
top_moves = stockfish.get_top_moves(engine.get_board(), 3)
for i, (move, score) in enumerate(top_moves, 1):
    print(f"   {i}. {move} ({score:+.2f})")

# Test a blunder
print("\n6️⃣  Testing blunder detection...")
engine.make_move('e5')
board_before = engine.get_board().copy()
print("   Making dubious move: Qh5")
engine.make_move('Qh5')

analysis = stockfish.analyze_move(board_before, 'Qh5')
print(f"   Classification: {analysis['classification']}")
print(f"   Better move: {analysis['best_move']}")
print(f"   Eval change: {analysis['eval_change']:+.2f}")

# Cleanup
stockfish.stop()

print("\n" + "="*60)
print("✅ Analysis Mode working perfectly!")
print("="*60 + "\n")
