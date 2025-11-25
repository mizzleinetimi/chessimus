#!/usr/bin/env python3
"""Test puzzle mode interactively"""

import sys
sys.path.insert(0, 'src')

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
from chess_game.renderer import BoardRenderer

print("🧩 Testing Puzzle Mode\n")

# Fetch puzzle
print("Fetching puzzle from Lichess...")
puzzle_json = LichessAPI.get_random_puzzle()
puzzle_data = PuzzleParser.parse(puzzle_json)

print(f"\n✅ Puzzle #{puzzle_data['id']}")
print(f"Rating: {puzzle_data['rating']}")
print(f"Themes: {', '.join(puzzle_data['themes'])}")

# Create engine
engine = PuzzleEngine(puzzle_data)
renderer = BoardRenderer(theme='default', use_unicode=True)

# Show board
print("\n" + renderer.render(engine.get_board()))

# Get hint
hint = engine.get_hint()
print(f"💡 Hint: The first move is {hint}")

# Test correct move
print(f"\n🧪 Testing correct move: {puzzle_data['moves'][0]}")
result, move = engine.check_move(puzzle_data['moves'][0])
print(f"Result: {result}")

if result == 'correct':
    print("✅ Correct move accepted!")
    print("\n" + renderer.render(engine.get_board()))
    print(f"💡 Next hint: {engine.get_hint()}")
else:
    print(f"❌ Failed: {result}")

# Test incorrect move
print("\n🧪 Testing incorrect move: e2e4")
board_before = engine.get_board().copy()
result, move = engine.check_move("e2e4")
print(f"Result: {result}")

if result == 'incorrect':
    print("✅ Incorrect move rejected correctly!")
else:
    print(f"❌ Should have rejected but got: {result}")

print("\n✅ Puzzle mode working correctly!")
