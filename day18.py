# Advent of Code 2022
# Day 18

from utils import setup, load
import re


DAY = 18


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    lines = load.lines(args.input)

    # load the cubes
    max_x = 0
    max_y = 0
    max_z = 0

    cubes = set()
    for line in lines:
        match = re.search(r"(\d+),(\d+),(\d+)", line)
        x = int(match.group(1))
        y = int(match.group(2))
        z = int(match.group(3))

        if x > max_x:
            max_x = x
        if y > max_y:
            max_y = y
        if z > max_z:
            max_z = z
        cubes.add((x, y, z))

    if args.part == 1:
        n_surfaces = 0
        for x, y, z in cubes:
            candidates = [
                (x + 1, y, z),
                (x - 1, y, z),
                (x, y + 1, z),
                (x, y - 1, z),
                (x, y, z + 1),
                (x, y, z - 1),
            ]
            for c in candidates:
                if c not in cubes:
                    n_surfaces += 1

        print("Result:", n_surfaces)

    if args.part == 2:
        outside = set()
        test = set()
        for x in range(max_x + 1):
            for y in range(max_y + 1):
                if (x, y, 0) not in cubes:
                    outside.add((x, y, 0))
                    test.add((x, y, 1))
                if (x, y, max_z) not in cubes:
                    outside.add((x, y, max_z))
                    test.add((x, y, max_z - 1))

        for x in range(max_x + 1):
            for z in range(max_z + 1):
                if (x, 0, z) not in cubes:
                    outside.add((x, 0, z))
                    test.add((x, 1, z))
                if (x, max_y, z) not in cubes:
                    outside.add((x, max_y, z))
                    test.add((x, max_y - 1, z))

        for y in range(max_y + 1):
            for z in range(max_z + 1):
                if (0, y, z) not in cubes:
                    outside.add((0, y, z))
                    test.add((1, y, z))
                if (max_x, y, z) not in cubes:
                    outside.add((max_x, y, z))
                    test.add((max_x - 1, y, z))

        while len(test) > 0:
            t = test.pop()
            if t not in cubes and t not in outside:
                outside.add(t)
                test.add((t[0] - 1, t[1], t[2]))
                test.add((t[0] + 1, t[1], t[2]))
                test.add((t[0], t[1] - 1, t[2]))
                test.add((t[0], t[1] + 1, t[2]))
                test.add((t[0], t[1], t[2] - 1))
                test.add((t[0], t[1], t[2] + 1))

        for x in range(max_x + 1):
            for y in range(max_y + 1):
                for z in range(max_z + 1):
                    if (x, y, z) not in outside:
                        cubes.add((x, y, z))

        n_surfaces = 0
        for x, y, z in cubes:
            candidates = [
                (x + 1, y, z),
                (x - 1, y, z),
                (x, y + 1, z),
                (x, y - 1, z),
                (x, y, z + 1),
                (x, y, z - 1),
            ]
            for c in candidates:
                if c not in cubes:
                    n_surfaces += 1

        print("Result", n_surfaces)


if __name__ == "__main__":
    main()
