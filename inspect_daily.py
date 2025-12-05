
import requests
import chess
import chess.pgn
from io import StringIO

def inspect_daily_puzzle():
    print("Fetching daily puzzle from Lichess...")
    try:
        response = requests.get("https://lichess.org/api/puzzle/daily")
        response.raise_for_status()
        data = response.json()
        
        puzzle_id = data['puzzle']['id']
        rating = data['puzzle']['rating']
        initial_ply = data['puzzle']['initialPly']
        solution = data['puzzle']['solution']
        pgn = data['game']['pgn']
        
        print(f"\nPuzzle ID: {puzzle_id}")
        print(f"Rating: {rating}")
        print(f"Initial Ply: {initial_ply}")
        print(f"Solution: {solution}")
        
        # Parse PGN to verify state
        pgn_io = StringIO(pgn)
        game = chess.pgn.read_game(pgn_io)
        board = game.board()
        
        print(f"\nReplaying PGN up to ply {initial_ply}...")
        for i, move in enumerate(game.mainline_moves()):
            if i >= initial_ply:
                break
            board.push(move)
            
        print(f"FEN after {initial_ply} plies: {board.fen()}")
        print(f"Turn: {'White' if board.turn == chess.WHITE else 'Black'}")
        
        # Check if solution moves are legal
        print("\nVerifying solution moves:")
        for move_uci in solution:
            try:
                move = chess.Move.from_uci(move_uci)
                if move in board.legal_moves:
                    san = board.san(move)
                    print(f"  {move_uci} ({san}) - Legal")
                    board.push(move)
                else:
                    print(f"  {move_uci} - ILLEGAL!")
            except Exception as e:
                print(f"  {move_uci} - Error: {e}")
                
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_daily_puzzle()
