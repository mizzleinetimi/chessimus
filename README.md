# 👻 Terminal Chess + Lichess Puzzles - Kiroween Submission

A spooky terminal-based chess application that stitches together multiple technologies into one haunted experience. Play chess, solve Lichess puzzles, battle the trash-talking Frankenstein AI, and learn with an AI coach.

**🎃 Kiroween Category: Frankenstein**

> *"Stitch together a chimera of technologies into one app. Bring together seemingly incompatible elements to build something unexpectedly powerful."*

## 🧟 The Monster We Built

This project is a true Frankenstein creation, stitching together:

- **python-chess** - Chess rules and board management
- **Lichess API** - Real-time puzzle fetching
- **Stockfish Engine** - Position analysis and move evaluation
- **OpenAI GPT-4** - AI coaching and dynamic trash talk
- **Terminal UI** - Spooky themed interface with Unicode pieces

## ✨ Features

### 🎮 Game Modes

| Mode | Description |
|------|-------------|
| **Play Mode** | Free play with move validation and undo |
| **Puzzle Mode** | Solve individual Lichess puzzles |
| **Endless Puzzles** | Rapid-fire puzzle stream with scoring |
| **Analysis Mode** | Play with real-time Stockfish evaluation |
| **Tutor Mode** | Learn with AI coach explanations |
| **VS AI** | Battle the Frankenstein AI with trash talk! |

### 👻 Spooky Elements

- Halloween-themed UI with ghost emojis
- Frankenstein AI opponent with dynamic trash talk
- Spooky color theme (purple/black)
- Ghostly piece set option
- AI-generated taunts that react to your moves

### 🧠 AI Features

- **Move Analysis**: Classifies moves as best/good/inaccuracy/mistake/blunder
- **Position Explanation**: AI coach explains who's winning and why
- **Dynamic Trash Talk**: GPT-4 generates context-aware taunts based on game state
- **Tactical Hints**: Get hints without revealing full solutions

## 🚀 Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/terminal-chess-puzzles.git
cd terminal-chess-puzzles

# Install dependencies
python3 -m pip install -r requirements.txt

# Optional: Install Stockfish for analysis features
brew install stockfish  # macOS
# or: apt install stockfish  # Linux

# Optional: Set OpenAI API key for AI coaching
export OPENAI_API_KEY="your-key-here"
```

## 🎮 Usage

```bash
python3 src/main.py
```

### Controls

- **Moves**: Enter in algebraic notation (`e4`, `Nf3`) or UCI (`e2e4`)
- **Square Query**: Type a square (`e2`) to see available moves highlighted
- **Commands**: `undo`, `hint`, `quit`, `exit`, `menu`

## 📸 Screenshots

```
========================================
♟️  TERMINAL CHESS + PUZZLES 👻
========================================
1. Play Mode - Free play
2. Puzzle Mode - Solve single puzzle
3. Endless Puzzles - Rapid-fire stream
4. Analysis Mode - Play with engine 🤖
5. Tutor Mode - Learn with AI coach 🧙
6. VS AI - Battle Frankenstein! 👻💀
7. Settings
8. Quit
========================================
```


---

## 🛠️ How Kiro Was Used

This project was built entirely with Kiro, leveraging its full suite of features for structured, efficient development.

### 📋 Spec-Driven Development

Kiro's spec system was instrumental in building this project methodically. Each major component had its own specification:

**`.kiro/specs/chess_engine.md`** - Defined requirements for:
- Board state management (FEN import/export)
- Move validation (algebraic and UCI notation)
- Game state detection (check, checkmate, stalemate)

**`.kiro/specs/puzzle_engine.md`** - Specified:
- Lichess API integration endpoints
- Puzzle data structure (ID, FEN, solution, rating, themes)
- Solution validation logic

**`.kiro/specs/terminal_renderer.md`** - Outlined:
- Unicode and ASCII piece sets
- Theme system (default + spooky)
- Square highlighting for legal moves

**`.kiro/specs/ui_navigation.md`** - Structured:
- Menu system and screen flow
- Input handling patterns
- Settings persistence

The spec-driven approach meant Kiro understood the full architecture before writing code, resulting in consistent implementations across all modules.

### 🎯 Steering Documents

Two steering files guided Kiro's code generation throughout the project:

**`.kiro/steering/code_style.md`**
```markdown
- Follow PEP 8
- Use type hints where helpful
- Docstrings for all classes and public methods
- Use try/except for external API calls
- Provide user-friendly error messages
```

**`.kiro/steering/ui_consistency.md`**
```markdown
- Use emojis for visual feedback (✅ ❌ 🎉 💡)
- Clear screen before major state changes
- Accept both lowercase and uppercase input
- Always provide way back to menu (quit, exit, menu)
- Press Enter to continue pattern
```

These steering docs ensured every screen and feature followed the same patterns, creating a cohesive user experience without manual enforcement.

### 🪝 Agent Hooks

Configured hooks for automated development workflows:

**`.kiro/hooks/format_on_save.json`** - Auto-format Python files with Black
**`.kiro/hooks/test_on_save.json`** - Run tests automatically on file save

### 💬 Vibe Coding Highlights

Key features built through natural conversation with Kiro:

1. **Frankenstein AI Opponent** - Described wanting "a spooky AI that trash talks based on how well I'm playing" and Kiro generated the full `AIOpponent` class with:
   - Difficulty levels (beginner → frankenstein)
   - Dynamic GPT-4 trash talk that analyzes board state
   - Move quality detection for contextual taunts

2. **Square Query Feature** - Asked "can I click a square to see where it can move?" and Kiro implemented visual highlighting across all game modes

3. **Multi-Theme System** - Requested "spooky Halloween theme" and got a complete theme system with purple/black colors and ghost pieces

### 🏆 Most Impressive Code Generation

The `AIOpponent` class showcases Kiro's ability to stitch together complex integrations:

```python
def _generate_dynamic_taunt(self, context: str, board: Optional[chess.Board] = None, 
                           move: Optional[str] = None) -> Optional[str]:
    """Generate dynamic trash talk using OpenAI with game context"""
    # Builds context with FEN, material balance, check status
    # Calls GPT-4o-mini with 3-second timeout
    # Falls back to static taunts if API unavailable
```

This single method combines:
- Chess position analysis
- Material counting
- OpenAI API integration
- Graceful fallback handling
- Timeout management for UX

---

## 📁 Project Structure

```
├── .kiro/
│   ├── hooks/          # Automation triggers
│   ├── specs/          # Feature specifications
│   └── steering/       # Code standards
├── src/
│   ├── ai/             # AI opponent, coach, Stockfish
│   ├── chess_game/     # Engine, renderer, input parser
│   ├── puzzles/        # Lichess API, puzzle engine
│   ├── settings/       # Configuration management
│   ├── ui/             # Screens and menus
│   └── main.py         # Entry point
├── requirements.txt
└── README.md
```

## 📄 License

MIT License - See [LICENSE](LICENSE) file

## 🎃 Happy Kiroween!

*Built with Kiro - the AI-powered IDE that helps you code like a monster* 👻
