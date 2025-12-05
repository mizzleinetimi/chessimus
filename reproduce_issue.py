
import chess
from puzzles.puzzle_parser import PuzzleParser
from puzzles.puzzle_engine import PuzzleEngine

# Mock puzzle data similar to what Lichess returns
mock_puzzle_json = {
    "game": {
        "pgn": "e4 e5 Nf3 Nc6 Bb5 a6 Ba4 Nf6 O-O Be7 Re1 b5 Bb3 d6 c3 O-O h3 Nb8 d4 Nbd7 c4 c6 cxd5 cxd5"
    },
    "puzzle": {
        "id": "00008",
        "initialPly": 20,
        "solution": ["e5d4", "f3d4", "c6d5"],
        "rating": 1500,
        "themes": ["opening"]
    }
}

print("Parsing puzzle...")
puzzle_data = PuzzleParser.parse(mock_puzzle_json)
print(f"FEN: {puzzle_data['fen']}")

print("\nInitializing PuzzleEngine...")
engine = PuzzleEngine(puzzle_data)
board = engine.get_board()

print(f"Board Move Stack: {board.move_stack}")
print(f"Board Move Stack Length: {len(board.move_stack)}")

if len(board.move_stack) == 0:
    print("\nBoard move stack is empty (expected).")
    if puzzle_data.get('last_move_uci'):
        print(f"SUCCESS: Found last move in puzzle data: {puzzle_data['last_move_uci']}")
    else:
        print("FAILURE: last_move_uci not found in puzzle data.")
else:
    print("\nMove stack is NOT empty.")
