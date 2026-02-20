# Utility functions for setting up the Advent of Code solutions.

import argparse
import os


def parse_command_line(day: int) -> argparse.Namespace:
    """Parses the command line."""
    default_input = os.path.join("data", f"day{day:02d}-input.txt")
    parser = argparse.ArgumentParser(description=f"Day {day} Solution.")
    parser.add_argument(
        "-i",
        "--input",
        type=str,
        default=default_input,
        help=f"Path to the input file (default: {default_input})",
    )
    parser.add_argument(
        "-p",
        "--part",
        type=int,
        choices=[1, 2],
        default=1,
        help="Specify Part 1 or 2 (default: 1)",
    )
    args = parser.parse_args()
    return args


def print_banner(day: int, part: int) -> None:
    """Prints a banner showing the given day and part."""
    print(f"=== Day {day}, part {part} ===")
