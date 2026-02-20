# Advent of Code 2022
# Day 4

from utils import setup, load
import re


DAY = 4


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # regex for parsing lines
    regex = r"(\d+)-(\d+),(\d+)-(\d+)"

    # Read the file
    lines = load.lines(args.input)

    contain_count = 0
    intersect_count = 0

    for line in lines:
        line = line.strip()

        match = re.search(regex, line)
        low1 = int(match.group(1))
        high1 = int(match.group(2))
        low2 = int(match.group(3))
        high2 = int(match.group(4))

        if low1 <= high2 and low2 <= high1:
            intersect_count = intersect_count + 1

        if (low1 <= low2 and high1 >= high2) or (low2 <= low1 and high2 >= high1):
            contain_count += 1

    if args.part == 1:
        print(f"Result: {contain_count}")
    if args.part == 2:
        print(f"Result: {intersect_count}")


if __name__ == "__main__":
    main()
