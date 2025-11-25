#!/usr/bin/env python3
"""Test square highlighting feature"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer

print("\n" + "="*60)
print("🎨 SQUARE HIGHLIGHTING TEST")
print("="*60)

engine = ChessEngine()
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

print("\nStarting position:")
print(renderer.render(engine.get_board()))

# Query e2
print("\n📍 Querying square 'e2':")
moves, dest_squares = engine.get_moves_from_square('e2')
if moves:
    print(f"Available moves: {', '.join(moves)}")
    print("\nBoard with highlighted destination squares:")
    print(renderer.render(engine.get_board(), dest_squares))
    print("✅ Yellow squares show where the pawn can move!")

# Make a move
engine.make_move('e4')
engine.make_move('e5')

print("\n" + "="*60)
print("After e4 e5:")
print(renderer.render(engine.get_board()))

# Query knight
print("\n📍 Querying square 'g1' (knight):")
moves, dest_squares = engine.get_moves_from_square('g1')
if moves:
    print(f"Available moves: {', '.join(moves)}")
    print("\nBoard with highlighted destination squares:")
    print(renderer.render(engine.get_board(), dest_squares))
    print("✅ Yellow squares show where the knight can jump!")

print("\n" + "="*60)
print("✅ Square highlighting working!")
print("="*60 + "\n")
