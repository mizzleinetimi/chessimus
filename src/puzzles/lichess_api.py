"""Lichess API integration for fetching puzzles"""

import requests

class LichessAPI:
    """Fetch puzzles from Lichess API"""
    
    BASE_URL = "https://lichess.org/api"
    
    # Pool of known valid puzzle IDs to simulate randomness
    # (Lichess doesn't have a random puzzle endpoint)
    PUZZLE_IDS = [
        'dDlYz', 'H5CTW', 'sdtQT', 'JfktH',  # Harvested
        '00008', '0000D', '000aY'            # Sequential/Known
    ]
    
    @staticmethod
    def get_random_puzzle():
        """Fetch a random puzzle from the pool"""
        try:
            import random
            puzzle_id = random.choice(LichessAPI.PUZZLE_IDS)
            return LichessAPI.get_puzzle_by_id(puzzle_id)
        except Exception as e:
            # Fallback to daily if random fails
            print(f"Failed to fetch random puzzle, falling back to daily: {e}")
            return LichessAPI.get_daily_puzzle()

    @staticmethod
    def get_daily_puzzle():
        """Fetch daily puzzle"""
        try:
            response = requests.get(f"{LichessAPI.BASE_URL}/puzzle/daily")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to fetch daily puzzle: {e}")
    
    @staticmethod
    def get_puzzle_by_id(puzzle_id):
        """Fetch specific puzzle by ID"""
        try:
            response = requests.get(f"{LichessAPI.BASE_URL}/puzzle/{puzzle_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to fetch puzzle {puzzle_id}: {e}")
