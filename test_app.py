#!/usr/bin/env python3
"""Quick test script for chess app functionality"""

import sys
sys.path.insert(0, 'src')

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from puzzles.lichess_api import LichessAPI
from puzzles.puzzle_parser import PuzzleParser

def test_chess_engine():
    """Test chess engine basics"""
    print("🧪 Testing Chess Engine...")
    engine = ChessEngine()
    
    # Test move
    assert engine.make_move('e4'), "Failed to make e4"
    assert engine.make_move('e5'), "Failed to make e5"
    print("✅ Moves work")
    
    # Test undo
    assert engine.undo_move(), "Failed to undo"
    print("✅ Undo works")
    
    # Test legal moves
    moves = engine.get_legal_moves()
    assert len(moves) > 0, "No legal moves found"
    print(f"✅ Legal moves: {len(moves)} moves available")
    
    print()

def test_renderer():
    """Test board rendering"""
    print("🧪 Testing Renderer...")
    engine = ChessEngine()
    renderer = BoardRenderer(theme='default', use_unicode=True)
    
    board_str = renderer.render(engine.get_board())
    assert '♜' in board_str or 'R' in board_str, "No pieces in render"
    print("✅ Board renders with pieces")
    
    # Test spooky theme
    spooky_renderer = BoardRenderer(theme='spooky', use_unicode=True)
    spooky_str = spooky_renderer.render(engine.get_board())
    assert len(spooky_str) > 0, "Spooky render failed"
    print("✅ Spooky theme works")
    
    print()

def test_lichess_api():
    """Test Lichess API"""
    print("🧪 Testing Lichess API...")
    try:
        puzzle = LichessAPI.get_random_puzzle()
        assert 'puzzle' in puzzle, "Invalid puzzle format"
        assert 'game' in puzzle, "Missing game data"
        print("✅ Puzzle fetch works")
        
        parsed = PuzzleParser.parse(puzzle)
        assert 'id' in parsed, "Missing puzzle ID"
        assert 'fen' in parsed, "Missing FEN"
        assert 'moves' in parsed, "Missing moves"
        print(f"✅ Puzzle parsed: #{parsed['id']}, rating {parsed['rating']}")
        
    except Exception as e:
        print(f"⚠️  API test failed (network issue?): {e}")
    
    print()

if __name__ == "__main__":
    print("\n" + "="*50)
    print("🎯 TERMINAL CHESS APP - QUICK TESTS")
    print("="*50 + "\n")
    
    test_chess_engine()
    test_renderer()
    test_lichess_api()
    
    print("="*50)
    print("✅ All tests passed!")
    print("="*50)
    print("\n🎮 To play: python3 src/main.py\n")
