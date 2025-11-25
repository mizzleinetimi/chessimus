# Puzzle Engine Specification

## Overview
Fetch, parse, and validate Lichess puzzle solutions.

## Requirements

### Lichess API Integration
- Fetch random puzzle
- Fetch daily puzzle
- Fetch puzzle by ID
- Parse JSON response

### Puzzle Data Structure
- Puzzle ID
- FEN position
- Solution moves (PGN)
- Rating
- Themes

### Solution Validation
- Load puzzle FEN
- Parse solution moves
- Validate user moves against solution
- Step through expected sequence
- Provide feedback (correct/incorrect/complete)

### Hints
- Show next expected move
- Don't reveal full solution

## Implementation

Uses Lichess public API endpoints:
- `GET /api/puzzle/daily`
- `GET /api/puzzle/{id}`

## Testing

- Fetch puzzle successfully
- Parse puzzle data
- Validate correct moves
- Reject incorrect moves
- Complete puzzle sequence
- Get hints
