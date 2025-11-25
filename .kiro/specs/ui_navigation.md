# UI Navigation Specification

## Overview
Menu system and screen navigation for terminal app.

## Requirements

### Main Menu
- Play Mode
- Puzzle Mode
- Endless Puzzles
- Settings
- Quit

### Play Mode Screen
- Display board
- Accept move input
- Show legal moves
- Undo moves
- Return to menu

### Puzzle Mode Screen
- Fetch puzzle
- Display puzzle info (rating, themes)
- Accept move input
- Validate against solution
- Show success/failure
- Return to menu

### Endless Mode Screen
- Loop puzzle fetching
- Track score
- Show statistics
- Quick transitions
- Return to menu

### Settings Screen
- Toggle theme
- Toggle Unicode/ASCII
- Toggle animations
- Save settings
- Return to menu

## Implementation

Screen-based architecture with config object passed to each screen.

## Testing

- Navigate between screens
- Settings persist across sessions
- Input validation
- Graceful error handling
