
import requests

def test_daily_date():
    print("Testing daily puzzle with date...")
    dates = ["2025-11-24", "2025-11-23", "2025-11-22"]
    
    for date in dates:
        url = f"https://lichess.org/api/puzzle/daily?date={date}"
        print(f"Trying {url}...", end='', flush=True)
        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json()
                print(f" SUCCESS! ID: {data['puzzle']['id']}")
            else:
                print(f" Failed ({response.status_code})")
        except Exception as e:
            print(f" Error: {e}")

if __name__ == "__main__":
    test_daily_date()
