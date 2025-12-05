
import requests

def test_user_activity():
    username = "Penguingim1"
    print(f"Testing puzzle activity for {username}...")
    url = f"https://lichess.org/api/user/{username}/puzzle-activity?max=20"
    
    try:
        response = requests.get(url)
        print(f"Status Code: {response.status_code}")
        
        if response.status_code == 200:
            # It returns NDJSON (newline delimited JSON)
            lines = response.text.strip().split('\n')
            print(f"Found {len(lines)} entries.")
            
            for i, line in enumerate(lines[:5]):
                print(f"Entry {i+1}: {line[:100]}...")
                
            # Extract IDs
            import json
            ids = []
            for line in lines:
                try:
                    data = json.loads(line)
                    if 'id' in data:
                        ids.append(data['id'])
                except:
                    pass
            
            print(f"\nExtracted {len(ids)} IDs: {ids}")
        else:
            print(f"Failed: {response.text}")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_user_activity()
