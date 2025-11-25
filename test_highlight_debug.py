#!/usr/bin/env python3
"""Debug highlighting"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
import chess

engine = ChessEngine()

# Query e2
moves, dest_squares = engine.get_moves_from_square('e2')
print(f"Moves from e2: {moves}")
print(f"Destination squares (raw): {dest_squares}")
print(f"Destination squares (names): {[chess.square_name(sq) for sq in dest_squares]}")

# The squares should be e3 (20) and e4 (28)
print(f"\ne3 = {chess.E3}, e4 = {chess.E4}")
