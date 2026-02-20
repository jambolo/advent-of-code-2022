# Advent of Code 2022
# Day 8

from utils import setup, load


DAY = 8

SIZE = 99


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    grid = []
    for line in lines:
        line = line.strip()
        row = []
        for c in line:
            row.append(int(c))
        if len(row) != SIZE:
            raise Exception(f"Row is the wrong size. It is {len(row)}, but it should be {SIZE}.")
        grid.append(row)
    if len(grid) != SIZE:
        raise Exception(f"Wrong number of rows. It is {len(grid)}, but it should be {SIZE}.")

    count = 4 * (SIZE - 1)  # count exterior cells
    max_score = 0

    # Look at each interior cell

    for i in range(1, SIZE - 1):
        for j in range(1, SIZE - 1):
            seen = False
            height = grid[i][j]

            # Check visibility from above
            if not seen:
                seen = True
                for k in range(i):
                    if grid[k][j] >= height:
                        seen = False
                        break

            # Check visibility from below
            if not seen:
                seen = True
                for k in range(i + 1, SIZE):
                    if grid[k][j] >= height:
                        seen = False
                        break

            # Check visibility from left
            if not seen:
                seen = True
                for k in range(j):
                    if grid[i][k] >= height:
                        seen = False
                        break

            # Check visibility from right
            if not seen:
                seen = True
                for k in range(j + 1, SIZE):
                    if grid[i][k] >= height:
                        seen = False
                        break

            # Count it if it can be seen
            if seen:
                count += 1

            # Check viewing score above
            view_above = 0
            for k in range(i - 1, -1, -1):
                view_above += 1
                if grid[k][j] >= height:
                    break

            # Check viewing score below
            view_below = 0
            for k in range(i + 1, SIZE):
                view_below += 1
                if grid[k][j] >= height:
                    break

            # Check viewing score left
            view_left = 0
            for k in range(j - 1, -1, -1):
                view_left += 1
                if grid[i][k] >= height:
                    break

            # Check viewing score right
            view_right = 0
            for k in range(j + 1, SIZE):
                view_right += 1
                if grid[i][k] >= height:
                    break

            score = view_above * view_below * view_left * view_right
            if score > max_score:
                max_score = score

    if args.part == 1:
        print(f"Result: {count}")
    if args.part == 2:
        print(f"Result: {max_score}")


if __name__ == "__main__":
    main()
