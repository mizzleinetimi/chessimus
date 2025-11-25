# Terminal Chess + Lichess Puzzle App 👻♟️

A terminal-based chess application with play mode and Lichess puzzle integration.

## Features

- **Play Mode**: Play legal chess moves in terminal
- **Puzzle Mode**: Fetch & solve Lichess puzzles
- **Endless Puzzle Run**: Rapid-fire puzzle stream
- **Polished Terminal UI**: Unicode pieces, color themes, animations
- **Settings**: Themes, modes, difficulty filters

## Installation

```bash
python3 -m pip install -r requirements.txt
```

## Usage

```bash
python3 src/main.py
```

## Quick Test

Run automated tests to verify everything works:

```bash
python3 test_app.py
```

## How to Play

### Play Mode
- Enter moves in algebraic notation: `e4`, `Nf3`, `Qh5`
- Or use UCI format: `e2e4`, `g1f3`
- Type a square (like `e2` or `g1`) to see available moves with visual highlighting
- Commands: `undo`, `moves`, `quit`

### Puzzle Mode
- Solve a single Lichess puzzle
- Enter the correct moves to complete the puzzle
- Type `hint` for help
- Type `quit` to return to menu

### Endless Mode
- Rapid-fire puzzle stream
- Score tracked automatically
- Keep solving until you quit

### Settings
- Toggle between default and spooky 👻 themes
- Switch Unicode pieces on/off
- Toggle large board (easier to read) or compact board
- Enable/disable animations

## Kiro Development

This project uses Kiro specs, hooks, and steering for structured development:

- `.kiro/specs/` - Feature specifications
- `.kiro/hooks/` - Auto-triggers for testing and formatting
- `.kiro/steering/` - Code standards and conventions

## Controls

- Enter moves in algebraic notation (e.g., `e4`, `Nf3`, `e2e4`)
- Type `undo` to undo last move
- Type `moves` to show legal moves
- Type `quit` to exit
