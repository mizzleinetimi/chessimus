"""Main menu and navigation"""

from ui.screens import PlayScreen, PuzzleScreen, SettingsScreen
from puzzles.endless_mode import EndlessMode

class MainMenu:
    """Main menu controller"""
    
    def __init__(self, config):
        """Initialize menu with config"""
        self.config = config
        self.running = True
    
    def run(self):
        """Display and handle main menu"""
        while self.running:
            self._display_menu()
            choice = input("\nSelect option: ").strip()
            self._handle_choice(choice)
    
    def _display_menu(self):
        """Display menu options"""
        print("\n" + "="*40)
        print("♟️  TERMINAL CHESS + PUZZLES 👻")
        print("="*40)
        print("\n1. Play Mode - Free play")
        print("2. Puzzle Mode - Solve single puzzle")
        print("3. Endless Puzzles - Rapid-fire stream")
        print("4. Settings")
        print("5. Quit")
        print("\n" + "="*40)
    
    def _handle_choice(self, choice):
        """Handle menu selection"""
        if choice == '1':
            screen = PlayScreen(self.config)
            screen.run()
        elif choice == '2':
            screen = PuzzleScreen(self.config)
            screen.run()
        elif choice == '3':
            mode = EndlessMode(self.config)
            mode.run()
        elif choice == '4':
            screen = SettingsScreen(self.config)
            screen.run()
        elif choice == '5':
            self.running = False
            print("\nThanks for playing! 👻\n")
        else:
            print("❌ Invalid option")
