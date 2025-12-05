"""Play against AI opponent with trash talk"""

from chess_game.engine import ChessEngine
from chess_game.renderer import BoardRenderer
from chess_game.input_parser import InputParser
from ai.ai_opponent import AIOpponent
import time


class AIOpponentScreen:
    """Play against AI opponent"""
    
    def __init__(self, config):
        self.config = config
        self.engine = ChessEngine()
        self.renderer = BoardRenderer(
            theme=config.get('theme', 'default'),
            use_unicode=config.get('use_unicode', True),
            large_board=config.get('large_board', True)
        )
    
    def _get_move_squares(self, move_str):
        """Extract from and to squares from move notation (e.g., 'e2e4' -> [12, 28])"""
        if not move_str or len(move_str) < 2:
            return []
        
        try:
            # Handle SAN notation (e.g., "Nf3", "exd5", "O-O")
            # Extract only the square coordinates
            squares = []
            
            # Remove capture notation, check, checkmate symbols
            clean_move = move_str.replace('x', '').replace('+', '').replace('#', '').replace('=', '')
            
            # For castling, return empty (can't easily highlight)
            if 'O' in clean_move or '0' in clean_move:
                return []
            
            # Find all square coordinates (letter + digit)
            import re
            square_pattern = r'[a-h][1-8]'
            found_squares = re.findall(square_pattern, clean_move)
            
            for sq in found_squares[-2:]:  # Take last 2 squares (from and to)
                if len(sq) == 2:
                    file = ord(sq[0]) - ord('a')
                    rank = int(sq[1]) - 1
                    if 0 <= file < 8 and 0 <= rank < 8:
                        squares.append(rank * 8 + file)
            
            return squares
        except Exception:
            return []  # Silently fail if parsing doesn't work
    
    def run(self):
        """Run AI opponent mode"""
        print("\n🤖 AI OPPONENT MODE")
        print("Play against the Frankenstein AI!\n")
        
        # Select difficulty
        print("Select difficulty:")
        print("1. Beginner 🟢")
        print("2. Intermediate 🟡")
        print("3. Strong 🔴")
        print("4. Frankenstein 👻💀 (MAXIMUM SPOOKINESS)")
        
        choice = input("\nDifficulty: ").strip()
        difficulty_map = {
            '1': 'beginner',
            '2': 'intermediate',
            '3': 'strong',
            '4': 'frankenstein'
        }
        difficulty = difficulty_map.get(choice, 'intermediate')
        
        # Initialize AI
        ai = AIOpponent(difficulty=difficulty, personality='spooky')
        if not ai.start():
            print("❌ AI engine not available!")
            input("\nPress Enter to return to menu...")
            return
        
        print(f"\n✅ AI ready at {difficulty} difficulty!")
        
        # Opening taunt
        taunt = ai.get_opening_taunt()
        if taunt:
            print(f"\n{taunt}")
        
        input("\nPress Enter to start...")
        
        try:
            player_last_move = None
            last_ai_move = None
            last_ai_message = ""  # Track AI's last move and taunt
            error_message = ""  # Track error messages
            
            while not self.engine.is_game_over():
                self.renderer.clear_screen()
                
                # Highlight only the last move (AI's move on player's turn)
                highlight_squares = []
                from_square = None
                if self.config.get('highlight_moves', True) and last_ai_move:
                    # Check if we have the tuple format (from, to, san)
                    if isinstance(last_ai_move, tuple) and len(last_ai_move) == 3:
                        from_square = last_ai_move[0]
                        highlight_squares = [last_ai_move[1]]
                    else:
                        # Fallback to old parsing method
                        move_squares = self._get_move_squares(last_ai_move)
                        if len(move_squares) >= 2:
                            from_square = move_squares[0]
                            highlight_squares = [move_squares[-1]]
                        else:
                            highlight_squares = move_squares
                
                print(self.renderer.render(self.engine.get_board(), highlight_squares, from_square))
                
                # Show last AI message if exists
                if last_ai_message:
                    print(last_ai_message)
                
                # Show error message if exists
                if error_message:
                    print(error_message)
                    error_message = ""  # Clear after displaying
                
                if self.engine.is_check():
                    if self.engine.get_board().turn:  # White's turn (player)
                        print("⚠️  You're in check!")
                    else:
                        print("👻 Boo! I put you in check!")
                
                # Player's turn
                print("\n💡 Commands: undo, hint, help, quit")
                user_input = input("Your move: ").strip()
                input_type, value = InputParser.parse(user_input)
                
                if input_type == 'command':
                    if value in ['quit', 'exit', 'menu']:
                        break
                    elif value == 'help':
                        print("\n📋 Available Commands:")
                        print("   undo  - Take back your last move")
                        print("   hint  - Ask for a hint (AI will mock you)")
                        print("   quit  - Return to main menu")
                        print("\n📍 Square Query: Type a square (e.g., 'e4') to see possible moves")
                        input("\nPress Enter to continue...")
                    elif value == 'undo':
                        # Undo both player and AI moves
                        if self.engine.undo_move() and self.engine.undo_move():
                            player_last_move = None
                            last_ai_move = None
                            last_ai_message = ""  # Clear AI message after undo
                        else:
                            error_message = "\n❌ No moves to undo"
                    elif value == 'hint':
                        error_message = "\n👻 No hints! Figure it out yourself, mortal!"
                
                elif input_type == 'move':
                    # Get the move object before making it
                    board_copy = self.engine.get_board().copy()
                    try:
                        move_obj = board_copy.parse_san(value)
                        player_from_sq = move_obj.from_square
                        player_to_sq = move_obj.to_square
                        player_last_move = (player_from_sq, player_to_sq, value)
                    except:
                        player_last_move = value
                    
                    if self.engine.make_move(value):
                        # Show board after player's move with highlighting
                        self.renderer.clear_screen()
                        if isinstance(player_last_move, tuple) and len(player_last_move) == 3:
                            print(self.renderer.render(self.engine.get_board(), [player_last_move[1]], player_last_move[0]))
                        else:
                            print(self.renderer.render(self.engine.get_board()))
                        
                        # AI reacts to player's move
                        try:
                            reaction = ai.get_response_to_player_move(
                                self.engine.get_board(), 
                                value
                            )
                            if reaction:
                                print(f"\n{reaction}")
                                time.sleep(1.5)
                        except Exception:
                            pass  # Silently skip if reaction fails
                        
                        # Check if game over after player move
                        if self.engine.is_game_over():
                            break
                        
                        # AI's turn - show board with player's move highlighted while AI thinks
                        self.renderer.clear_screen()
                        if isinstance(player_last_move, tuple) and len(player_last_move) == 3:
                            print(self.renderer.render(self.engine.get_board(), [player_last_move[1]], player_last_move[0]))
                        else:
                            print(self.renderer.render(self.engine.get_board()))
                        
                        print("\n🤖 AI is thinking...")
                        time.sleep(0.8)  # Dramatic pause
                        
                        try:
                            ai_move = ai.get_move(self.engine.get_board())
                            if ai_move:
                                # Get the actual move object before making it
                                board_copy = self.engine.get_board().copy()
                                try:
                                    move_obj = board_copy.parse_san(ai_move)
                                    from_sq = move_obj.from_square
                                    to_sq = move_obj.to_square
                                    # Store as tuple for later use
                                    last_ai_move = (from_sq, to_sq, ai_move)
                                except:
                                    last_ai_move = ai_move
                                
                                self.engine.make_move(ai_move)
                                
                                # AI trash talks
                                try:
                                    taunt = ai.get_move_taunt(
                                        self.engine.get_board(),
                                        ai_move,
                                        player_last_move
                                    )
                                except Exception as e:
                                    taunt = "👻 Boo!"  # Fallback if trash talk fails
                                
                                # Store AI message to display on next turn
                                move_display = last_ai_move[2] if isinstance(last_ai_move, tuple) else ai_move
                                last_ai_message = f"\n🤖 AI plays: {move_display}"
                                if taunt:
                                    last_ai_message += f"\n{taunt}"
                                
                                time.sleep(1.5)  # Brief pause to read AI's move
                            else:
                                print("\n❌ AI failed to find a move!")
                                break
                        except Exception as e:
                            print(f"\n❌ AI error: {e}")
                            break
                    else:
                        # Check if it's a square query
                        moves, dest_squares = self.engine.get_moves_from_square(value)
                        if moves:
                            error_message = f"\n📍 Moves from {value}: {', '.join(moves)}"
                        else:
                            error_message = "\n❌ Illegal move - try again\n👻 Can't even make a legal move? Pathetic!"
            
            # Game over
            self.renderer.clear_screen()
            print(self.renderer.render(self.engine.get_board()))
            
            if self.engine.is_checkmate():
                # Determine winner
                if self.engine.get_board().turn:  # White to move = Black won
                    print("\n🎉 CHECKMATE! You won!")
                    taunt = ai.get_checkmate_taunt(i_won=False)
                else:  # Black to move = White won
                    print("\n💀 CHECKMATE! AI wins!")
                    taunt = ai.get_checkmate_taunt(i_won=True)
                
                if taunt:
                    print(f"\n{taunt}")
            elif self.engine.is_game_over():
                print("\n🤝 Game over - Draw!")
                print("👻 I'll accept this draw... for now!")
        
        finally:
            ai.stop()
            input("\nPress Enter to return to menu...")
