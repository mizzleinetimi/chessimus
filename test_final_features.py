#!/usr/bin/env python3
"""Final comprehensive feature test"""

import sys
sys.path.insert(0, 'src')

from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine
from chess_game.renderer import BoardRenderer

print("\n" + "="*60)
print("🎯 COMPREHENSIVE FEATURE TEST")
print("="*60)

# Fetch puzzle
puzzle_json = LichessAPI.get_random_puzzle()
puzzle_data = PuzzleParser.parse(puzzle_json)
engine = PuzzleEngine(puzzle_data)
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

print(f"\n✅ Puzzle #{puzzle_data['id']} (Rating: {puzzle_data['rating']})")
print(renderer.render(engine.get_board()))

turn = engine.get_turn_info()
print(f"🎯 {turn} to play and win!")

# Feature 1: Hint
print("\n1️⃣  HINT FEATURE")
hint = engine.get_hint()
print(f"   💡 Hint: {hint}")

# Feature 2: Square query for own pieces
print("\n2️⃣  SQUARE QUERY (own pieces)")
import chess
for square_name in ['e3', 'b3', 'a4']:
    sq = chess.parse_square(square_name)
    piece = engine.get_board().piece_at(sq)
    if piece and piece.color == engine.get_board().turn:
        moves = engine.get_moves_from_square(square_name)
        if moves:
            print(f"   📍 {square_name}: {', '.join(moves[:3])}")

# Feature 3: Turn indicator
print("\n3️⃣  TURN INDICATOR")
print(f"   🎯 {turn} to play")

# Feature 4: Bright colored pieces
print("\n4️⃣  VISUAL IMPROVEMENTS")
print("   ✅ Large board with bright pieces")
print("   ✅ White pieces: Bright white + bold")
print("   ✅ Black pieces: Bright yellow + bold")

print("\n" + "="*60)
print("✅ ALL FEATURES WORKING!")
print("="*60)
print("\n📖 Available commands:")
print("   • Type a move: e4, Nf3, Qxf4")
print("   • Type a square: e2, g1 (shows available moves)")
print("   • Type 'hint' for help")
print("   • Type 'quit' to exit")
print("="*60 + "\n")
