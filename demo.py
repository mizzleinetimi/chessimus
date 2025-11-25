#!/usr/bin/env python3
"""Quick demo of all features"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser

print("\n" + "="*50)
print("♟️  TERMINAL CHESS + PUZZLES DEMO 👻")
print("="*50)

# Demo 1: Chess Engine
print("\n1️⃣  CHESS ENGINE DEMO")
print("-" * 50)
engine = ChessEngine()
renderer = BoardRenderer(theme='default', use_unicode=True)

print("Starting position:")
print(renderer.render(engine.get_board()))

print("Making moves: e4, e5, Nf3, Nc6")
engine.make_move('e4')
engine.make_move('e5')
engine.make_move('Nf3')
engine.make_move('Nc6')

print(renderer.render(engine.get_board()))

# Demo 2: Spooky Theme
print("\n2️⃣  SPOOKY THEME 👻🎃")
print("-" * 50)
spooky_renderer = BoardRenderer(theme='spooky', use_unicode=True)
print(spooky_renderer.render(engine.get_board()))

# Demo 3: Puzzle
print("\n3️⃣  LICHESS PUZZLE")
print("-" * 50)
print("Fetching puzzle...")
puzzle_json = LichessAPI.get_random_puzzle()
puzzle_data = PuzzleParser.parse(puzzle_json)

print(f"\nPuzzle #{puzzle_data['id']}")
print(f"Rating: {puzzle_data['rating']}")
print(f"Themes: {', '.join(puzzle_data['themes'])}")
print(f"Solution: {' → '.join(puzzle_data['moves'][:3])}...")

puzzle_engine = ChessEngine(puzzle_data['fen'])
print(renderer.render(puzzle_engine.get_board()))

print("\n" + "="*50)
print("✅ All features working!")
print("="*50)
print("\n🎮 To play: python3 src/main.py")
print("📖 Commands: e4, Nf3, undo, moves, quit\n")
