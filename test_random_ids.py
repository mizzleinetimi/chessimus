
import requests
import random
import string
import time

def generate_random_id(length=5):
    chars = string.ascii_letters + string.digits
    return ''.join(random.choice(chars) for _ in range(length))

def test_random_ids():
    print("Harvesting random puzzle IDs...")
    success_count = 0
    attempts = 100
    valid_ids = []
    
    for i in range(attempts):
        puzzle_id = generate_random_id()
        url = f"https://lichess.org/api/puzzle/{puzzle_id}"
        # print(f"[{i+1}/{attempts}] Trying {url}...", end='', flush=True)
        
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(f"SUCCESS! ID: {puzzle_id}")
                valid_ids.append(puzzle_id)
                success_count += 1
            # else:
            #     print(f" Failed ({response.status_code})")
        except Exception as e:
            print(f" Error: {e}")
            
        time.sleep(0.1)
        
    print(f"\nFound {len(valid_ids)} IDs: {valid_ids}")

if __name__ == "__main__":
    test_random_ids()
