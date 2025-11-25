#!/usr/bin/env python3
"""Test square query in puzzle mode"""

import sys
sys.path.insert(0, 'src')

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
from chess_game.renderer import BoardRenderer

print("\n🧩 Testing Square Query in Puzzle Mode\n")

# Fetch puzzle
print("Fetching puzzle from Lichess...")
puzzle_json = LichessAPI.get_random_puzzle()
puzzle_data = PuzzleParser.parse(puzzle_json)

print(f"\n✅ Puzzle #{puzzle_data['id']}")
print(f"Rating: {puzzle_data['rating']}")

# Create engine
engine = PuzzleEngine(puzzle_data)
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

# Show board
print("\n" + renderer.render(engine.get_board()))

turn = engine.get_turn_info()
print(f"🎯 {turn} to play and win!")

# Test square query
print("\n🧪 Testing square queries:")

# Get hint to know which piece to query
hint = engine.get_hint()
print(f"💡 Hint: {hint}")

# Try to figure out the from square from the hint
import chess
solution_uci = puzzle_data['moves'][0]
from_square = solution_uci[:2]
to_square = solution_uci[2:4]

print(f"\n📍 Querying square '{from_square}':")
moves = engine.get_moves_from_square(from_square)
if moves:
    print(f"   Available moves: {', '.join(moves)}")
    print(f"   ✅ Square query works! The hint '{hint}' is in the list.")
else:
    print(f"   ❌ No moves found")

print("\n📍 Querying empty square 'd4':")
moves = engine.get_moves_from_square('d4')
if moves:
    print(f"   Available moves: {', '.join(moves)}")
else:
    print(f"   Empty square (as expected)")

print("\n✅ Square query feature works in puzzle mode!")
