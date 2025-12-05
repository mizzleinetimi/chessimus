
import requests

def test_training_mix():
    print("Testing /training/mix redirect...")
    url = "https://lichess.org/training/mix"
    
    try:
        response = requests.get(url, allow_redirects=False)
        print(f"Status Code: {response.status_code}")
        print(f"Headers: {response.headers}")
        
        if response.status_code == 200:
            print("Page loaded. Searching for puzzle ID...")
            content = response.text
            
            # Look for puzzle ID patterns
            # Pattern 1: "puzzle":{"id":"xxxxx"}
            if '"puzzle":{"id":"' in content:
                start = content.find('"puzzle":{"id":"') + 15
                end = content.find('"', start)
                puzzle_id = content[start:end]
                print(f"Found ID via JSON: {puzzle_id}")
                
                # Verify
                api_url = f"https://lichess.org/api/puzzle/{puzzle_id}"
                print(f"Verifying API: {api_url}")
                api_resp = requests.get(api_url)
                if api_resp.status_code == 200:
                    print("SUCCESS: Valid puzzle ID found in HTML.")
                else:
                    print(f"FAILURE: API fetch failed ({api_resp.status_code})")
            else:
                print("Could not find puzzle ID in HTML.")
                print(f"Preview: {content[:500]}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_training_mix()
