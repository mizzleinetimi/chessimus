"""Terminal board renderer with Unicode pieces and colors"""

import os
from colorama import Fore, Back, Style, init

init(autoreset=True)

# Highlight colors for last moves
HIGHLIGHT_FROM = Back.YELLOW + Style.BRIGHT  # From square (where piece came from)
HIGHLIGHT_TO = Back.RED + Style.BRIGHT  # To square (where piece moved to)

class BoardRenderer:
    """Render chess board in terminal"""
    
    UNICODE_PIECES = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '♔',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '♚',
    }
    
    ASCII_PIECES = {
        'P': 'P', 'N': 'N', 'B': 'B', 'R': 'R', 'Q': 'Q', 'K': 'K',
        'p': 'p', 'n': 'n', 'b': 'b', 'r': 'r', 'q': 'q', 'k': 'k',
    }
    
    SPOOKY_PIECES = {
        'P': '♙', 'N': '♘', 'B': '♗', 'R': '♖', 'Q': '♕', 'K': '👻',
        'p': '♟', 'n': '♞', 'b': '♝', 'r': '♜', 'q': '♛', 'k': '🎃',
    }
    
    def __init__(self, theme='default', use_unicode=True, large_board=True):
        """Initialize renderer with theme"""
        self.theme = theme
        self.use_unicode = use_unicode
        self.large_board = large_board
        self.pieces = self._get_piece_set()
    
    def _get_piece_set(self):
        """Get piece set based on theme"""
        if self.theme == 'spooky':
            return self.SPOOKY_PIECES
        elif self.use_unicode:
            return self.UNICODE_PIECES
        else:
            return self.ASCII_PIECES
    
    def render(self, board, highlighted_squares=None, from_square=None):
        """Render board to terminal
        
        Args:
            board: chess.Board object
            highlighted_squares: list of squares to highlight (to squares)
            from_square: single square to highlight as origin (from square)
        """
        if self.large_board:
            return self._render_large(board, highlighted_squares, from_square)
        else:
            return self._render_compact(board, highlighted_squares, from_square)
    
    def _render_large(self, board, highlighted_squares=None, from_square=None):
        """Render large board with extra spacing"""
        highlighted_squares = highlighted_squares or []
        from_squares = [from_square] if from_square is not None else []
        
        output = []
        output.append("\n    ╔════════════════════════════════════════════╗")
        
        for rank in range(7, -1, -1):
            # Top padding line
            line_top = f"    ║"
            for file in range(8):
                square = rank * 8 + file
                is_light = (rank + file) % 2 == 1
                is_from = square in from_squares
                is_to = square in highlighted_squares
                
                if is_from:
                    bg = HIGHLIGHT_FROM
                elif is_to:
                    bg = HIGHLIGHT_TO
                elif is_light:
                    bg = Back.WHITE if self.theme != 'spooky' else Back.MAGENTA
                else:
                    bg = Back.BLUE if self.theme != 'spooky' else Back.BLACK
                
                line_top += f"{bg}     {Style.RESET_ALL}"
            line_top += "║"
            output.append(line_top)
            
            # Piece line
            line = f"  {rank + 1} ║"
            for file in range(8):
                square = rank * 8 + file
                piece = board.piece_at(square)
                
                # Determine square color
                is_light = (rank + file) % 2 == 1
                is_from = square in from_squares
                is_to = square in highlighted_squares
                
                # Apply colors
                if is_from:
                    bg = HIGHLIGHT_FROM
                elif is_to:
                    bg = HIGHLIGHT_TO
                elif is_light:
                    bg = Back.WHITE if self.theme != 'spooky' else Back.MAGENTA
                else:
                    bg = Back.BLUE if self.theme != 'spooky' else Back.BLACK
                
                # Get piece symbol with consistent colors per side
                if piece:
                    symbol = self.pieces.get(piece.symbol(), piece.symbol())
                    # White pieces: bright cyan (always)
                    # Black pieces: bright yellow (always)
                    if piece.color:  # White pieces
                        fg = Fore.CYAN + Style.BRIGHT
                    else:  # Black pieces
                        fg = Fore.YELLOW + Style.BRIGHT
                else:
                    symbol = ' '
                    fg = ''
                
                line += f"{bg}{fg}  {symbol}  {Style.RESET_ALL}"
            
            line += "║"
            output.append(line)
            
            # Bottom padding line
            line_bottom = f"    ║"
            for file in range(8):
                square = rank * 8 + file
                is_light = (rank + file) % 2 == 1
                is_from = square in from_squares
                is_to = square in highlighted_squares
                
                if is_from:
                    bg = HIGHLIGHT_FROM
                elif is_to:
                    bg = HIGHLIGHT_TO
                elif is_light:
                    bg = Back.WHITE if self.theme != 'spooky' else Back.MAGENTA
                else:
                    bg = Back.BLUE if self.theme != 'spooky' else Back.BLACK
                
                line_bottom += f"{bg}     {Style.RESET_ALL}"
            line_bottom += "║"
            output.append(line_bottom)
        
        output.append("    ╚════════════════════════════════════════════╝")
        output.append("       a    b    c    d    e    f    g    h\n")
        
        return '\n'.join(output)
    
    def _render_compact(self, board, highlighted_squares=None, from_square=None):
        """Render compact board (original size)"""
        highlighted_squares = highlighted_squares or []
        from_squares = [from_square] if from_square is not None else []
        
        output = []
        output.append("\n  ┌─────────────────┐")
        
        for rank in range(7, -1, -1):
            line = f"{rank + 1} │ "
            for file in range(8):
                square = rank * 8 + file
                piece = board.piece_at(square)
                
                # Determine square color
                is_light = (rank + file) % 2 == 1
                is_from = square in from_squares
                is_to = square in highlighted_squares
                
                # Apply colors
                if is_from:
                    bg = HIGHLIGHT_FROM
                elif is_to:
                    bg = HIGHLIGHT_TO
                elif is_light:
                    bg = Back.WHITE if self.theme != 'spooky' else Back.MAGENTA
                else:
                    bg = Back.BLUE if self.theme != 'spooky' else Back.BLACK
                
                # Get piece symbol with consistent colors per side
                if piece:
                    symbol = self.pieces.get(piece.symbol(), piece.symbol())
                    # White pieces: bright cyan (always)
                    # Black pieces: bright yellow (always)
                    if piece.color:  # White pieces
                        fg = Fore.CYAN + Style.BRIGHT
                    else:  # Black pieces
                        fg = Fore.YELLOW + Style.BRIGHT
                else:
                    symbol = ' '
                    fg = ''
                
                line += f"{bg}{fg}{symbol} {Style.RESET_ALL}"
            
            line += "│"
            output.append(line)
        
        output.append("  └─────────────────┘")
        output.append("    a b c d e f g h\n")
        
        return '\n'.join(output)
    
    def clear_screen(self):
        """Clear terminal screen"""
        os.system('clear' if os.name != 'nt' else 'cls')
    
    def animate_move(self, board_before, board_after):
        """Simple animation by redrawing"""
        self.clear_screen()
        print(self.render(board_after))
