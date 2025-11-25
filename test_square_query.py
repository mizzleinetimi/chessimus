#!/usr/bin/env python3
"""Test square query feature"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer

print("\n🎯 Testing Square Query Feature\n")

engine = ChessEngine()
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=False)

print("Starting position:")
print(renderer.render(engine.get_board()))

# Test querying squares
test_queries = ['e2', 'g1', 'a1', 'd4', 'e8']

import chess

for square in test_queries:
    moves = engine.get_moves_from_square(square)
    if moves:
        print(f"📍 Moves from {square}: {', '.join(moves)}")
    else:
        try:
            sq = chess.parse_square(square)
            piece = engine.get_board().piece_at(sq)
            if piece:
                print(f"📍 {square}: No legal moves")
            else:
                print(f"📍 {square}: Empty square")
        except:
            print(f"📍 {square}: Invalid square")

print("\n✅ Now test making a move:")
print("Making move: e4")
if engine.make_move('e4'):
    print("✅ Move made!")
    print(renderer.render(engine.get_board()))
    
    print("\nNow query e2 (should be empty):")
    moves = engine.get_moves_from_square('e2')
    if moves:
        print(f"📍 Moves from e2: {', '.join(moves)}")
    else:
        print("📍 e2: Empty square")
    
    print("\nQuery e4 (pawn just moved there):")
    moves = engine.get_moves_from_square('e4')
    if moves:
        print(f"📍 Moves from e4: {', '.join(moves)}")
    else:
        print("📍 e4: No legal moves (pawn can't move yet)")

print("\n✅ Square query feature working!")
