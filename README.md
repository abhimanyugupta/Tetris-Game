# Tetris Clone (Python + Pygame)

A clean baseline Tetris clone built for iterative development in Codex.

## Current scope (Milestone 0 + 1)
- 10x20 board
- 7 tetrominoes
- 7-bag randomizer
- Gravity, movement, rotation
- Soft drop and hard drop
- Piece locking and line clears
- Score, level, and line tracking
- Pause and game-over restart flow

## Controls
- Left / A: Move left
- Right / D: Move right
- Up / X: Rotate clockwise
- Z: Rotate counter-clockwise
- Down / S: Soft drop
- Space: Hard drop
- ESC: Pause / Resume
- R: Restart (on game over)

## Run
1. Install dependencies:
   `pip install -r requirements.txt`
2. Start game:
   `python main.py`

## Next milestones
- SRS wall kicks + lock delay
- Hold piece + richer preview UX
- Advanced scoring (B2B, T-Spins, perfect clears)
- Multiple modes (Marathon/Sprint/Ultra)
