# Chess Engine Specification

## Overview
Chess rule engine wrapper for board state, move validation, and game logic.

## Requirements

### Board State Management
- Initialize board with standard starting position
- Load board from FEN string
- Export current position as FEN
- Track move history

### Move Validation
- Parse moves in algebraic notation (e4, Nf3)
- Parse moves in UCI format (e2e4)
- Validate moves against legal moves
- Reject illegal moves

### Game State Detection
- Detect check
- Detect checkmate
- Detect stalemate
- Detect game over conditions

### Move Operations
- Make move
- Undo move
- Get list of legal moves

## Implementation

Uses `python-chess` library as the underlying engine.

## Testing

- Load FEN and verify board state
- Make legal moves and verify success
- Attempt illegal moves and verify rejection
- Undo moves and verify board state
- Detect check/checkmate correctly
