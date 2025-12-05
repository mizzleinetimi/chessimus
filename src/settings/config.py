"""Configuration management"""

import json
import os

class Config:
    """Manage application settings"""
    
    DEFAULT_CONFIG = {
        'theme': 'default',
        'use_unicode': True,
        'animations': True,
        'large_board': True,
        'highlight_moves': True,
        'puzzle_min_rating': 1000,
        'puzzle_max_rating': 2200,
        'coach_style': 'normal',
        'show_explanations': True
    }
    
    CONFIG_FILE = 'settings.json'
    
    def __init__(self):
        """Load or create config"""
        self.settings = self._load()
    
    def _load(self):
        """Load settings from file"""
        if os.path.exists(self.CONFIG_FILE):
            try:
                with open(self.CONFIG_FILE, 'r') as f:
                    return {**self.DEFAULT_CONFIG, **json.load(f)}
            except:
                return self.DEFAULT_CONFIG.copy()
        return self.DEFAULT_CONFIG.copy()
    
    def save(self):
        """Save settings to file"""
        with open(self.CONFIG_FILE, 'w') as f:
            json.dump(self.settings, f, indent=2)
    
    def get(self, key, default=None):
        """Get setting value"""
        return self.settings.get(key, default)
    
    def set(self, key, value):
        """Set setting value"""
        self.settings[key] = value
    
    def toggle(self, key):
        """Toggle boolean setting"""
        if key in self.settings and isinstance(self.settings[key], bool):
            self.settings[key] = not self.settings[key]
