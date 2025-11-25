"""Parse and validate user input for chess moves"""

class InputParser:
    """Parse user input for chess commands and moves"""
    
    COMMANDS = ['quit', 'exit', 'undo', 'moves', 'help', 'menu', 'hint']
    
    @staticmethod
    def parse(user_input):
        """
        Parse user input and return (command_type, value)
        Returns: ('command', 'quit') or ('move', 'e4')
        """
        cleaned = user_input.strip().lower()
        
        if not cleaned:
            return ('empty', None)
        
        if cleaned in InputParser.COMMANDS:
            return ('command', cleaned)
        
        # Assume it's a move
        return ('move', user_input.strip())
    
    @staticmethod
    def normalize_move(move_str):
        """Normalize move string (e.g., 'E4' -> 'e4')"""
        return move_str.strip()
