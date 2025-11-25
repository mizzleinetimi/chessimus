#!/usr/bin/env python3
"""Test large board rendering"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer

print("\n" + "="*60)
print("📏 BOARD SIZE COMPARISON")
print("="*60)

engine = ChessEngine()
engine.make_move('e4')
engine.make_move('e5')
engine.make_move('Nf3')
engine.make_move('Nc6')

print("\n🔹 COMPACT BOARD (original)")
print("-" * 60)
compact = BoardRenderer(theme='default', use_unicode=True, large_board=False)
print(compact.render(engine.get_board()))

print("\n🔸 LARGE BOARD (easier to read)")
print("-" * 60)
large = BoardRenderer(theme='default', use_unicode=True, large_board=True)
print(large.render(engine.get_board()))

print("\n👻 LARGE SPOOKY BOARD")
print("-" * 60)
spooky = BoardRenderer(theme='spooky', use_unicode=True, large_board=True)
print(spooky.render(engine.get_board()))

print("="*60)
print("✅ Large board is now the default!")
print("   Toggle in Settings menu (option 3)")
print("="*60 + "\n")
