
import chess

def test_fallback_logic():
    print("Testing fallback logic...")
    pgn_str = "1. e4 e6 2. d4 d5"
    initial_ply = 4
    
    board = chess.Board()
    moves = pgn_str.split()
    
    moves_pushed = 0
    for i, move_san in enumerate(moves):
        # The BUG: checking i against initial_ply
        if i >= initial_ply:
            print(f"Breaking at token index {i} (token: {move_san})")
            break
            
        try:
            if move_san.endswith('.'):
                continue
                
            board.push_san(move_san)
            moves_pushed += 1
            print(f"Pushed {move_san}")
        except:
            pass
            
    print(f"\nTotal moves pushed: {moves_pushed}")
    print(f"Expected moves: {initial_ply}")
    print(f"Board FEN: {board.fen()}")
    
    if moves_pushed != initial_ply:
        print("FAILURE: Fallback logic pushed incorrect number of moves.")
    else:
        print("SUCCESS: Fallback logic correct.")

if __name__ == "__main__":
    test_fallback_logic()
