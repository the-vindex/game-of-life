# Game of Life — Grid Display Setup

**Date:** 2026-03-30
**Scope:** Project setup only — no game logic. Grid rendering + click toggling.

## Overview

A pygame-based 2D grid display for Game of Life. The project establishes the visual foundation: a 50×50 grid where cells can be toggled on/off by clicking. No simulation logic is included.

## Files

### `grid.py`

Contains the `Grid` class and all display constants.

**Constants (module-level):**
- `COLS = 50`, `ROWS = 50`
- `CELL_SIZE = 12` (pixels per cell)
- `COLOR_BG` — background / dead cell color
- `COLOR_ALIVE` — live cell fill color
- `COLOR_GRID` — grid line color

**`Grid` class:**
- `cells: list[list[bool]]` — 50×50 2D list, all `False` on init
- `toggle(row, col)` — flips `cells[row][col]`
- `draw(surface)` — iterates all cells, fills alive ones, then draws grid lines on top

### `main.py`

Entry point. Handles pygame lifecycle and user input.

- Initializes pygame, creates a 600×600 window (`COLS * CELL_SIZE` × `ROWS * CELL_SIZE`)
- Creates a `Grid` instance
- Event loop:
  - `QUIT` → exit
  - `MOUSEBUTTONDOWN` → converts `(px, py)` to `(row, col)` via `// CELL_SIZE`, calls `grid.toggle(row, col)`
- Each frame: clear surface, call `grid.draw(surface)`, `pygame.display.flip()`

## Dependencies

- `pygame` (install via `pip install pygame`)

## Out of Scope

- Game of Life rules / next-generation logic
- File save/load
- Speed controls or play/pause
