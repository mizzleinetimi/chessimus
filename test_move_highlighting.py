#!/usr/bin/env python3
"""Test move highlighting"""

from src.chess_game.engine import ChessEngine
from src.chess_game.renderer import BoardRenderer

def test_highlighting():
    """Test move highlighting"""
    engine = ChessEngine()
    renderer = BoardRenderer(large_board=True)
    
    # Make a move
    engine.make_move('e2e4')
    
    # Highlight e2 and e4 (squares 12 and 28)
    # e2 = file 4 (e), rank 1 (2-1) = 1*8 + 4 = 12
    # e4 = file 4 (e), rank 3 (4-1) = 3*8 + 4 = 28
    highlight_squares = [12, 28]
    
    print("Testing move highlighting for e2e4:")
    print(f"Highlighting squares: {highlight_squares}")
    print(renderer.render(engine.get_board(), highlight_squares))
    
    # Also test with a different move
    engine.make_move('e7e5')
    # e7 = file 4, rank 6 = 6*8 + 4 = 52
    # e5 = file 4, rank 4 = 4*8 + 4 = 36
    highlight_squares = [52, 36]
    
    print("\nTesting move highlighting for e7e5:")
    print(f"Highlighting squares: {highlight_squares}")
    print(renderer.render(engine.get_board(), highlight_squares))

if __name__ == '__main__':
    test_highlighting()
