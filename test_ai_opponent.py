#!/usr/bin/env python3
"""Test AI Opponent with trash talk"""

import sys
sys.path.insert(0, 'src')

import chess
from ai.ai_opponent import AIOpponent
from chess_game.renderer import BoardRenderer

print("\n" + "="*70)
print("👻 AI OPPONENT TEST - FRANKENSTEIN TRASH TALK")
print("="*70)

# Initialize AI
ai = AIOpponent(difficulty='intermediate', personality='spooky')
renderer = BoardRenderer(theme='spooky', use_unicode=True, large_board=True)

if not ai.start():
    print("❌ Stockfish not available")
    sys.exit(1)

print("\n✅ Frankenstein AI ready!")

# Opening taunt
print("\n" + "="*70)
print("OPENING TAUNT:")
print("="*70)
taunt = ai.get_opening_taunt()
print(f"\n{taunt}")

# Simulate a game
board = chess.Board()

print("\n" + "="*70)
print("GAME SIMULATION:")
print("="*70)

# Move 1: Player plays e4
print("\n1️⃣  Player plays e4")
board.push_san('e4')
print(renderer.render(board))

# AI responds
ai_move = ai.get_move(board)
print(f"\n🤖 AI plays: {ai_move}")
board.push_san(ai_move)
taunt = ai.get_move_taunt(board, ai_move, 'e4')
print(f"{taunt}")

# Move 2: Player plays Nf3
print("\n\n2️⃣  Player plays Nf3")
board.push_san('Nf3')

# AI reacts
reaction = ai.get_response_to_player_move(board, 'Nf3')
print(f"\n{reaction}")

# AI responds
ai_move = ai.get_move(board)
print(f"\n🤖 AI plays: {ai_move}")
board.push_san(ai_move)
taunt = ai.get_move_taunt(board, ai_move, 'Nf3')
print(f"{taunt}")

# Move 3: Player makes a blunder
print("\n\n3️⃣  Player plays d4? (dubious)")
board.push_san('d4')

# AI reacts to dubious move
reaction = ai.get_response_to_player_move(board, 'd4')
print(f"\n{reaction}")

print(renderer.render(board))

# AI responds
ai_move = ai.get_move(board)
print(f"\n🤖 AI plays: {ai_move}")
board.push_san(ai_move)
taunt = ai.get_move_taunt(board, ai_move, 'd4')
print(f"{taunt}")

# Test checkmate taunts
print("\n\n" + "="*70)
print("CHECKMATE TAUNTS:")
print("="*70)

print("\n👻 If AI wins:")
print(ai.get_checkmate_taunt(i_won=True))

print("\n👻 If player wins:")
print(ai.get_checkmate_taunt(i_won=False))

# Cleanup
ai.stop()

print("\n" + "="*70)
print("✅ Frankenstein AI trash talk working perfectly!")
print("="*70 + "\n")
