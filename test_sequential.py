
import requests

def test_sequential_ids():
    print("Testing sequential puzzle IDs...")
    ids = ["00001", "00002", "00003", "00004", "00005", "00008", "0000D", "000aY"]
    
    for pid in ids:
        url = f"https://lichess.org/api/puzzle/{pid}"
        print(f"Trying {url}...", end='', flush=True)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                print(" SUCCESS!")
            else:
                print(f" Failed ({response.status_code})")
        except Exception as e:
            print(f" Error: {e}")

if __name__ == "__main__":
    test_sequential_ids()
