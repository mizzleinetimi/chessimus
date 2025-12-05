
import requests
import chess
import chess.pgn
from io import StringIO

def analyze_puzzle_moves():
    print("Fetching daily puzzle...")
    response = requests.get("https://lichess.org/api/puzzle/daily")
    data = response.json()
    
    pgn = data['game']['pgn']
    initial_ply = data['puzzle']['initialPly']
    solution = data['puzzle']['solution']
    
    print(f"Initial Ply: {initial_ply}")
    print(f"Solution: {solution}")
    
    pgn_io = StringIO(pgn)
    game = chess.pgn.read_game(pgn_io)
    
    print("\nMoves around initialPly:")
    moves = list(game.mainline_moves())
    
    start = max(0, initial_ply - 2)
    end = min(len(moves), initial_ply + 2)
    
    for i in range(start, end):
        move = moves[i]
        prefix = ">>> " if i == initial_ply else "    "
        print(f"{prefix}Ply {i}: {move.uci()}")
        
    # Check overlap
    pgn_move_at_ply = moves[initial_ply].uci() if initial_ply < len(moves) else "None"
    print(f"\nPGN move at initialPly ({initial_ply}): {pgn_move_at_ply}")
    print(f"First solution move: {solution[0]}")
    
    if pgn_move_at_ply == solution[0]:
        print("MATCH: The first move of the solution IS the move at initialPly in the PGN.")
    else:
        print("NO MATCH.")

if __name__ == "__main__":
    analyze_puzzle_moves()
