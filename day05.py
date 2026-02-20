# Advent of Code 2022
# Day 5

from utils import setup, load
import re


DAY = 5


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    # Parse the crates
    # The first 8 lines contain the crates. There are 9 piles.
    # The contents of the crates start at column 1 and are every 4 characters apart

    piles = [[], [], [], [], [], [], [], [], []]

    for i in range(8):
        line = lines[i].strip()
        for p in range(9):
            if p * 4 + 1 >= len(line):
                break
            crate = line[p * 4 + 1]
            if crate != " ":
                piles[p].insert(0, crate)

    # Draw the piles
    #    draw_piles(piles)

    # Process the move commands: move {count} from {from} to {to}
    # Move commands start at line 10

    moveRe = r"move (\d+) from (\d+) to (\d+)"
    i = 10
    while i < len(lines):
        line = lines[i].strip()
        match = re.search(moveRe, line)
        count = int(match.group(1))
        fromPile = int(match.group(2)) - 1
        toPile = int(match.group(3)) - 1

        # Move the crates
        if args.part == 1:
            for j in range(count):
                crate = piles[fromPile].pop()
                piles[toPile].append(crate)
        if args.part == 2:
            piles[toPile].extend(piles[fromPile][-count:])
            piles[fromPile] = piles[fromPile][:-count]

        i = i + 1

    # Draw the result
    #    draw_piles(piles)

    # List the tops of the piles as specified
    print("Result:", end="")
    for pile in piles:
        print(f"{pile[-1]}", end="")
    print("")


if __name__ == "__main__":
    main()
