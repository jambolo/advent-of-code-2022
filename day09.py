# Advent of Code 2022
# Day 9

from utils import setup, load
import re


DAY = 9


def follow(head: tuple[int, int], tail: tuple[int, int]) -> tuple[int, int]:
    dx = 0
    dy = 0
    if head[0] > tail[0] + 1:
        dx = 1
        if head[1] > tail[1]:
            dy = 1
        elif head[1] < tail[1]:
            dy = -1
    elif head[0] < tail[0] - 1:
        dx = -1
        if head[1] > tail[1]:
            dy = 1
        elif head[1] < tail[1]:
            dy = -1
    elif head[1] > tail[1] + 1:
        dy = 1
        if head[0] > tail[0]:
            dx = 1
        elif head[0] < tail[0]:
            dx = -1
    elif head[1] < tail[1] - 1:
        dy = -1
        if head[0] > tail[0]:
            dx = 1
        elif head[0] < tail[0]:
            dx = -1
    return (tail[0] + dx, tail[1] + dy)


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    if args.part == 1:
        number_of_knots = 2
    if args.part == 2:
        number_of_knots = 10

    knots = []
    for i in range(number_of_knots):
        knots.append((0, 0))

    visited = {knots[number_of_knots - 1]}

    for line in lines:
        line = line.strip()

        match = re.search(r"(\w)\s+(\d+)", line)
        direction = match.group(1)
        distance = int(match.group(2))
        for i in range(distance):
            # Move the head
            if direction == "U":
                knots[0] = (knots[0][0], knots[0][1] + 1)
            elif direction == "D":
                knots[0] = (knots[0][0], knots[0][1] - 1)
            elif direction == "R":
                knots[0] = (knots[0][0] + 1, knots[0][1])
            elif direction == "L":
                knots[0] = (knots[0][0] - 1, knots[0][1])

            # Move the rest of the knots
            for i in range(1, number_of_knots):
                knots[i] = follow(knots[i - 1], knots[i])

            visited.add(knots[number_of_knots - 1])

    print(f"Result: {len(visited)}")


if __name__ == "__main__":
    main()
