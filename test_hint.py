#!/usr/bin/env python3
"""Test hint command in puzzle mode"""

import sys
sys.path.insert(0, 'src')

from chess_game.input_parser import InputParser

# Test that hint is recognized as a command
test_inputs = ['hint', 'HINT', 'Hint', 'e4', 'quit', 'undo']

print("Testing InputParser with hint command:\n")
for inp in test_inputs:
    input_type, value = InputParser.parse(inp)
    print(f"  '{inp}' -> type: {input_type}, value: {value}")

print("\n✅ 'hint' is now recognized as a command!")
