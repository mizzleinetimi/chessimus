#!/usr/bin/env python3
"""Debug puzzle fetching and rendering"""

import sys
sys.path.insert(0, 'src')

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
from chess_game.renderer import BoardRenderer
import json

print("🔍 Fetching puzzle from Lichess...")
puzzle_json = LichessAPI.get_random_puzzle()

print("\n📦 Raw JSON:")
print(json.dumps(puzzle_json, indent=2))

print("\n🔧 Parsing puzzle...")
puzzle_data = PuzzleParser.parse(puzzle_json)

print("\n📋 Parsed data:")
for key, value in puzzle_data.items():
    print(f"  {key}: {value}")

print("\n🎮 Creating puzzle engine...")
engine = PuzzleEngine(puzzle_data)

print("\n♟️  Rendering board:")
renderer = BoardRenderer(theme='default', use_unicode=True)
print(renderer.render(engine.get_board()))

print(f"\n💡 First hint: {engine.get_hint()}")
print(f"📝 Solution moves: {puzzle_data['moves']}")
