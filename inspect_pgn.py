
import requests
import json

def inspect_lichess_puzzle():
    print("Fetching random puzzle from Lichess...")
    try:
        response = requests.get("https://lichess.org/api/puzzle/daily")
        response.raise_for_status()
        data = response.json()
        
        pgn = data['game']['pgn']
        print(f"\nPGN Preview (first 100 chars): {pgn[:100]}")
        print(f"PGN has move numbers? {'1.' in pgn}")
        
        initial_ply = data['puzzle']['initialPly']
        print(f"Initial Ply: {initial_ply}")
        
        # Test splitting
        tokens = pgn.split()
        print(f"First 10 tokens: {tokens[:10]}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_lichess_puzzle()
