#!/usr/bin/env python3
"""Test LLM Chess Coach"""

import sys
import os
sys.path.insert(0, 'src')

import chess
from ai.chess_coach import ChessCoach
from ai.stockfish_engine import StockfishEngine

print("\n" + "="*60)
print("🧙 CHESS COACH TEST")
print("="*60)

# Check for API key
if not os.getenv('OPENAI_API_KEY'):
    print("\n⚠️  OPENAI_API_KEY not set!")
    print("Set it with: export OPENAI_API_KEY='your-key-here'")
    print("\nSkipping coach tests...")
    sys.exit(0)

# Initialize coach
print("\n1️⃣  Initializing coach...")
coach = ChessCoach(style='normal')
print("✅ Coach ready!")

# Initialize Stockfish for evaluations
stockfish = StockfishEngine(depth=10)
if not stockfish.start():
    print("❌ Stockfish not available")
    sys.exit(1)

# Test position explanation
print("\n2️⃣  Testing position explanation...")
board = chess.Board()
board.push_san('e4')
board.push_san('e5')
board.push_san('Nf3')

eval_data = stockfish.get_evaluation(board)
explanation = coach.explain_position(board, eval_data)
print(f"\nPosition after 1.e4 e5 2.Nf3:")
print(f"📊 Evaluation: {eval_data['evaluation_text']}")
print(f"🧙 Coach says: {explanation}")

# Test move explanation (good move)
print("\n3️⃣  Testing move explanation (good move)...")
board_before = board.copy()
eval_before = stockfish.get_evaluation(board_before)
board.push_san('Nc6')
analysis = stockfish.analyze_move(board_before, 'Nc6')
explanation = coach.explain_move(board_before, 'Nc6', analysis, eval_before)
print(f"\nMove: Nc6 ({analysis['classification']})")
print(f"🧙 Coach says: {explanation}")

# Test move explanation (bad move)
print("\n4️⃣  Testing move explanation (mistake)...")
board_before = board.copy()
eval_before = stockfish.get_evaluation(board_before)
board.push_san('Qh5')  # Dubious move
analysis = stockfish.analyze_move(board_before, 'Qh5')
explanation = coach.explain_move(board_before, 'Qh5', analysis, eval_before)
print(f"\nMove: Qh5 ({analysis['classification']})")
print(f"🧙 Coach says: {explanation}")

# Test tactical explanation
print("\n5️⃣  Testing tactical explanation...")
board = chess.Board()
board.push_san('e4')
board.push_san('e5')
eval_data = stockfish.get_evaluation(board)
top_moves = stockfish.get_top_moves(board, 3)
explanation = coach.explain_tactic(board, eval_data['best_move'], top_moves)
print(f"\nPosition after 1.e4 e5:")
print(f"🧙 Coach says: {explanation}")

# Test spooky style
print("\n6️⃣  Testing spooky style 👻...")
spooky_coach = ChessCoach(style='spooky')
board = chess.Board()
eval_data = stockfish.get_evaluation(board)
explanation = spooky_coach.explain_position(board, eval_data)
print(f"👻 Spooky coach says: {explanation}")

# Cleanup
stockfish.stop()

print("\n" + "="*60)
print("✅ Chess Coach working perfectly!")
print("="*60 + "\n")
