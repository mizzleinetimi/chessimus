
from src.puzzles.lichess_api import LichessAPI

def verify_randomness():
    print("Verifying random puzzle selection...")
    ids = set()
    attempts = 10
    
    for i in range(attempts):
        print(f"Fetch {i+1}...", end='', flush=True)
        try:
            puzzle = LichessAPI.get_random_puzzle()
            pid = puzzle['puzzle']['id']
            print(f" Got {pid}")
            ids.add(pid)
        except Exception as e:
            print(f" Error: {e}")
            
    print(f"\nUnique IDs found: {len(ids)}/{attempts}")
    print(f"IDs: {ids}")
    
    if len(ids) > 1:
        print("SUCCESS: Multiple puzzles fetched.")
    else:
        print("FAILURE: Only one puzzle fetched (or none).")

if __name__ == "__main__":
    verify_randomness()
