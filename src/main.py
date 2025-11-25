#!/usr/bin/env python3
"""Terminal Chess + Lichess Puzzle App - Main Entry Point"""

import sys
from ui.menu import MainMenu
from settings.config import Config

def main():
    """Application entry point"""
    try:
        config = Config()
        menu = MainMenu(config)
        menu.run()
    except KeyboardInterrupt:
        print("\n\nThanks for playing! 👻")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
