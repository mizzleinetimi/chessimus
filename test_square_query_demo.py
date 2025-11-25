#!/usr/bin/env python3
"""Demo of square query feature"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer

print("\n" + "="*50)
print("🎯 SQUARE QUERY FEATURE DEMO")
print("="*50)

engine = ChessEngine()
renderer = BoardRenderer(theme='default', use_unicode=True, large_board=True)

print("\nStarting position:")
print(renderer.render(engine.get_board()))

print("💡 TIP: Type a square (like 'e2') to see what can move from there!")
print("="*50)

# Demo 1: Query a square
print("\n1️⃣  Query: 'e2'")
moves = engine.get_moves_from_square('e2')
print(f"   📍 Moves from e2: {', '.join(moves)}")

# Demo 2: Make a move normally
print("\n2️⃣  Move: 'e4' (makes the move)")
engine.make_move('e4')
print("   ✅ Pawn moved to e4")

# Black's turn
engine.make_move('e5')

# Demo 3: Query knight
print("\n3️⃣  Query: 'g1'")
moves = engine.get_moves_from_square('g1')
if moves:
    print(f"   📍 Moves from g1: {', '.join(moves)}")
else:
    print("   📍 g1: No legal moves")

# Demo 4: Make knight move
print("\n4️⃣  Move: 'Nf3' (makes the move)")
engine.make_move('Nf3')
print("   ✅ Knight moved to f3")

print("\nCurrent position:")
print(renderer.render(engine.get_board()))

print("="*50)
print("✅ How it works:")
print("   • Type a move (e4, Nf3) → Makes the move")
print("   • Type a square (e2, g1) → Shows available moves")
print("   • Pawn moves like 'e4' work normally")
print("   • Empty squares show 'Empty square'")
print("="*50 + "\n")
