#!/usr/bin/env python3
"""Debug puzzle square"""

import sys
sys.path.insert(0, 'src')

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
import chess

# Fetch puzzle
puzzle_json = LichessAPI.get_random_puzzle()
puzzle_data = PuzzleParser.parse(puzzle_json)
engine = PuzzleEngine(puzzle_data)

print(f"FEN: {puzzle_data['fen']}")
print(f"Solution: {puzzle_data['moves']}")
print(f"First move UCI: {puzzle_data['moves'][0]}")

# Parse the first move
first_move_uci = puzzle_data['moves'][0]
from_sq = first_move_uci[:2]
to_sq = first_move_uci[2:4]

print(f"\nFrom square: {from_sq}")
print(f"To square: {to_sq}")

# Check what's on the from square
sq = chess.parse_square(from_sq)
piece = engine.get_board().piece_at(sq)
print(f"Piece on {from_sq}: {piece}")

# Get moves from that square
moves = engine.get_moves_from_square(from_sq)
print(f"Moves from {from_sq}: {moves}")

# Try a white piece
print("\nTrying white pieces:")
for square_name in ['e3', 'b3', 'a4', 'f3']:
    sq = chess.parse_square(square_name)
    piece = engine.get_board().piece_at(sq)
    if piece:
        moves = engine.get_moves_from_square(square_name)
        print(f"  {square_name} ({piece}): {moves}")
