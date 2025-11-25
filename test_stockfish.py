#!/usr/bin/env python3
"""Test Stockfish integration"""

import sys
sys.path.insert(0, 'src')

import chess
from ai.stockfish_engine import StockfishEngine

print("\n🤖 Testing Stockfish Integration\n")

# Try to start engine
engine = StockfishEngine(depth=10)
if not engine.start():
    print("❌ Stockfish not found!")
    print("\n💡 To install Stockfish:")
    print("   macOS: brew install stockfish")
    print("   Linux: sudo apt-get install stockfish")
    print("   Or download from: https://stockfishchess.org/download/")
    sys.exit(1)

print("✅ Stockfish engine started!")

# Test position
board = chess.Board()
board.push_san('e4')
board.push_san('e5')

print("\nPosition after 1.e4 e5:")
print(board)

# Get evaluation
print("\n📊 Position Evaluation:")
eval_data = engine.get_evaluation(board)
print(f"   Score: {eval_data['score']:.2f}")
print(f"   Assessment: {eval_data['evaluation_text']}")
print(f"   Best move: {eval_data['best_move']}")

# Get top moves
print("\n🎯 Top 3 Moves:")
top_moves = engine.get_top_moves(board, 3)
for i, (move, score) in enumerate(top_moves, 1):
    print(f"   {i}. {move} ({score:+.2f})")

# Analyze a move
print("\n🔍 Move Analysis:")
print("   Testing move: Nf3")
analysis = engine.analyze_move(board, 'Nf3')
print(f"   Classification: {analysis['classification']}")
print(f"   Eval change: {analysis['eval_change']:+.2f}")

print("\n   Testing move: Qh5 (dubious)")
analysis = engine.analyze_move(board, 'Qh5')
print(f"   Classification: {analysis['classification']}")
print(f"   Eval change: {analysis['eval_change']:+.2f}")

# Cleanup
engine.stop()
print("\n✅ All tests passed!")
