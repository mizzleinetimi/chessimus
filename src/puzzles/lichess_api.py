"""Lichess API integration for fetching puzzles"""

import requests

class LichessAPI:
    """Fetch puzzles from Lichess API"""
    
    BASE_URL = "https://lichess.org/api"
    
    @staticmethod
    def get_random_puzzle():
        """Fetch a random puzzle"""
        try:
            response = requests.get(f"{LichessAPI.BASE_URL}/puzzle/daily")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to fetch puzzle: {e}")
    
    @staticmethod
    def get_daily_puzzle():
        """Fetch daily puzzle"""
        return LichessAPI.get_random_puzzle()
    
    @staticmethod
    def get_puzzle_by_id(puzzle_id):
        """Fetch specific puzzle by ID"""
        try:
            response = requests.get(f"{LichessAPI.BASE_URL}/puzzle/{puzzle_id}")
            response.raise_for_status()
            return response.json()
        except Exception as e:
            raise Exception(f"Failed to fetch puzzle {puzzle_id}: {e}")
