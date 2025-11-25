#!/usr/bin/env python3
"""Demo of AI features - Stockfish + LLM Coach"""

import sys
import os
sys.path.insert(0, 'src')

import chess
from ai.stockfish_engine import StockfishEngine
from ai.chess_coach import ChessCoach
from chess_game.renderer import BoardRenderer

print("\n" + "="*70)
print("🤖 + 🧙 = FRANKENSTEIN CHESS AI DEMO")
print("="*70)

# Check API key
if not os.getenv('OPENAI_API_KEY'):
    print("\n⚠️  Set API key first:")
    print("   export OPENAI_API_KEY='your-key'")
    sys.exit(1)

# Initialize
stockfish = StockfishEngine(depth=12)
coach = ChessCoach(style='normal')
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

if not stockfish.start():
    print("❌ Stockfish not found")
    sys.exit(1)

print("\n✅ Stockfish engine ready")
print("✅ AI coach ready")

# Demo game
board = chess.Board()

print("\n" + "="*70)
print("DEMO: Learning from mistakes")
print("="*70)

# Move 1: Good opening
print("\n1️⃣  White plays e4 (good opening)")
print(renderer.render(board))

eval_before = stockfish.get_evaluation(board)
board.push_san('e4')
analysis = stockfish.analyze_move(chess.Board(), 'e4')

print(f"\n🤖 Stockfish: {analysis['classification']} move")
print(f"   Eval: {eval_before['score']:+.2f} → {analysis['eval_after']:+.2f}")

explanation = coach.explain_move(chess.Board(), 'e4', analysis, eval_before)
print(f"\n🧙 Coach: {explanation}")

# Move 2: Black responds
print("\n\n2️⃣  Black plays e5")
board.push_san('e5')
print(renderer.render(board))

# Move 3: White makes a mistake
print("\n\n3️⃣  White plays Qh5? (premature queen move)")
board_before = board.copy()
eval_before = stockfish.get_evaluation(board_before)
board.push_san('Qh5')
analysis = stockfish.analyze_move(board_before, 'Qh5')

print(renderer.render(board))
print(f"\n🤖 Stockfish: {analysis['classification']} move!")
print(f"   Eval change: {analysis['eval_change']:+.2f}")
print(f"   Better move: {analysis['best_move']}")

explanation = coach.explain_move(board_before, 'Qh5', analysis, eval_before)
print(f"\n🧙 Coach: {explanation}")

# Show tactical explanation
print("\n\n4️⃣  What should White have done?")
board_correct = chess.Board()
board_correct.push_san('e4')
board_correct.push_san('e5')

eval_data = stockfish.get_evaluation(board_correct)
top_moves = stockfish.get_top_moves(board_correct, 3)

print(f"\n🤖 Top 3 moves:")
for i, (move, score) in enumerate(top_moves, 1):
    print(f"   {i}. {move} ({score:+.2f})")

explanation = coach.explain_tactic(board_correct, eval_data['best_move'], top_moves)
print(f"\n🧙 Coach: {explanation}")

# Cleanup
stockfish.stop()

print("\n" + "="*70)
print("✅ This is the power of Stockfish + LLM coaching!")
print("="*70)
print("\n💡 Try Tutor Mode in the app to experience this live!")
print("   Run: python3 src/main.py → Option 5\n")
