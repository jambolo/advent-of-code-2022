# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

Advent of Code 2022 solutions in Python. All 25 days are complete. Solutions use algorithms ranging from simple linear scans to complex graph algorithms (A*, Dijkstra's), simulation, interval merging, and more. See README.md for a detailed breakdown of algorithms used per day.

## Running Solutions

```bash
python3 day01.py                          # Run day 1, part 1 with default input
python3 day01.py -p 2                     # Run day 1, part 2
python3 day01.py -i data/day01-test.txt   # Run with test input
```

All solutions use `utils.setup.parse_command_line(DAY)` which provides `-i`/`--input` (default: `data/dayNN-input.txt`) and `-p`/`--part` (1 or 2, default: 1).

## Testing & Linting

```bash
pytest                              # Run all tests
pytest tests/test_intervals.py      # Run specific test file
ruff format . --check               # Check formatting without changes
ruff check .                         # Lint code
```

CI (GitHub Actions) runs ruff format check, ruff lint, and pytest on Python 3.12.

## Code Architecture

### Utils Package

- `setup.py`: CLI argument parsing and banner printing
- `pathfinding.py`: A* and Dijkstra's algorithms for shortest-path problems
- `interval.py`: Interval merging, normalization, and set operations (union, intersection, subtraction) for range-based problems
- `load.py`: File loading utilities

### Day Solutions

Each day is a standalone script (`dayNN.py`) with the following pattern:

1. Parse command-line args via `setup.parse_command_line(DAY)`
2. Load input via `load.lines()` or `load.string()`
3. Solve part 1 and/or part 2 based on `args.part`
4. Print result to stdout

No external dependencies beyond Python stdlib; only ruff and pytest for development.

## Code Conventions

- Standalone Python scripts, one per day (`day01.py` through `day25.py`)
- Input files in `data/` directory with `utf-8-sig` encoding (BOM-aware)
- F-strings for string formatting
- Solutions print answers to stdout
- Max line length: 132 (per `.flake8` config)
- Test files in `tests/` cover utilities only (pathfinding, intervals), not day solutions
