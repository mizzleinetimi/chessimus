
import chess

def test_san_parsing():
    print("Testing SAN parsing for R1xc4...")
    
    # Setup a board where R1xc4 might be valid
    # White Rooks at c1 and c8. Black piece at c4.
    # Turn: White.
    board = chess.Board(None) # Empty board
    
    # Place pieces
    board.set_piece_at(chess.C1, chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.C8, chess.Piece(chess.ROOK, chess.WHITE))
    board.set_piece_at(chess.C4, chess.Piece(chess.PAWN, chess.BLACK))
    board.set_piece_at(chess.E1, chess.Piece(chess.KING, chess.WHITE))
    board.set_piece_at(chess.E8, chess.Piece(chess.KING, chess.BLACK))
    
    board.turn = chess.WHITE
    
    print(f"Board FEN: {board.fen()}")
    print(board)
    
    # Check legal moves
    print("\nLegal moves:")
    for move in board.legal_moves:
        print(f"{move.uci()} : {board.san(move)}")
        
    # Try to parse R1xc4
    move_str = "R1xc4"
    print(f"\nParsing '{move_str}'...")
    try:
        move = board.parse_san(move_str)
        print(f"Success! Parsed as {move.uci()}")
    except Exception as e:
        print(f"Failed to parse: {e}")

    # Try to parse R8xc4
    move_str = "R8xc4"
    print(f"\nParsing '{move_str}'...")
    try:
        move = board.parse_san(move_str)
        print(f"Success! Parsed as {move.uci()}")
    except Exception as e:
        print(f"Failed to parse: {e}")

if __name__ == "__main__":
    test_san_parsing()
