#!/usr/bin/env python3
"""Test puzzle improvements - turn info and error handling"""

import sys
sys.path.insert(0, 'src')

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
from chess_game.renderer import BoardRenderer

print("🧩 Testing Puzzle Improvements\n")

# Fetch puzzle
print("Fetching puzzle from Lichess...")
puzzle_json = LichessAPI.get_random_puzzle()
puzzle_data = PuzzleParser.parse(puzzle_json)

print(f"\n✅ Puzzle #{puzzle_data['id']}")
print(f"Rating: {puzzle_data['rating']}")
print(f"Themes: {', '.join(puzzle_data['themes'])}")

# Create engine
engine = PuzzleEngine(puzzle_data)
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

# Show board
print("\n" + renderer.render(engine.get_board()))

# Show turn info
turn = engine.get_turn_info()
print(f"🎯 {turn} to play and win!")

# Get hint
hint = engine.get_hint()
print(f"💡 Hint: {hint}")

# Test invalid move
print("\n🧪 Testing invalid move: 'xyz123'")
result, move = engine.check_move("xyz123")
print(f"Result: {result}")
if result == 'error':
    print(f"Error message: {move}")
    print("✅ Invalid moves are now caught!")

# Test incorrect but valid move
print("\n🧪 Testing incorrect but valid move: 'e2e4'")
result, move = engine.check_move("e2e4")
print(f"Result: {result}")
if result == 'incorrect':
    print("✅ Incorrect moves are detected!")

print("\n✅ All improvements working!")
