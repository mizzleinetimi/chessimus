# Terminal Renderer Specification

## Overview
Render chess board in terminal with Unicode pieces and color themes.

## Requirements

### Piece Sets
- Unicode pieces (♜ ♞ ♟)
- ASCII fallback (R N P)
- Spooky theme (👻 🎃)

### Board Display
- 8x8 grid with coordinates
- Alternating square colors
- Piece colors (white/black)
- Highlighted squares for legal moves

### Themes
- Default: Blue/white squares
- Spooky: Purple/black squares with ghost pieces

### Screen Management
- Clear screen
- Redraw board
- Simple move animations

## Implementation

Uses `colorama` for terminal colors and ANSI escape codes.

## Testing

- Render empty board
- Render starting position
- Render with highlighted squares
- Test both Unicode and ASCII modes
- Test theme switching
