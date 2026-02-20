# Advent of Code 2022
# Day 14

from utils import setup, load
import json


DAY = 14


EMPTY = 0
ROCK = 1
SAND = 2

START_X = 500
START_Y = 0


def place_rocks(board: list[list[int]], v0: list[int], v1: list[int], x0: int, y0: int) -> None:
    if v0[0] == v1[0]:
        # vertical
        x = v0[0] - x0
        for y in range(min(v0[1], v1[1]) - y0, max(v0[1], v1[1]) - y0 + 1):
            board[y][x] = ROCK
    else:
        # horizontal
        y = v0[1] - y0
        for x in range(min(v0[0], v1[0]) - x0, max(v0[0], v1[0]) - x0 + 1):
            board[y][x] = ROCK


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    # Parse the input after converting it to json for easy parsing
    multisegments = []
    for line in lines:
        line = "[[" + line.strip() + "]]"
        line = line.replace("->", "],[")
        line = json.loads(line)
        multisegments.append(line)

    # Find the limits of the board
    min_x = multisegments[0][0][0]
    min_y = 0
    max_x = multisegments[0][0][0]
    max_y = multisegments[0][0][1]
    for m in multisegments:
        for vertex in m:
            if vertex[0] < min_x:
                min_x = vertex[0]
            if vertex[0] > max_x:
                max_x = vertex[0]
            if vertex[1] < min_y:
                min_y = vertex[1]
            if vertex[1] > max_y:
                max_y = vertex[1]

    width = max_x - min_x + 1
    height = max_y - min_y + 1

    # Part 2: add the floor two below the lowest point
    if args.part == 2:
        max_y += 2
        min_x = min(min_x, START_X - height - 2)
        max_x = max(max_x, START_X + height + 2)
        width = max_x - min_x + 1
        height = max_y - min_y + 1
        multisegments.append([[min_x, max_y], [max_x, max_y]])

    # Create the board
    board = [[EMPTY] * width for i in range(height)]

    for m in multisegments:
        v0 = m[0]
        for i in range(1, len(m)):
            v1 = m[i]
            place_rocks(board, v0, v1, min_x, min_y)
            v0 = v1

    # draw_board(board)

    # Drop the sand

    done = False
    nSand = 0
    while not done:
        x = START_X - min_x
        y = START_Y - min_y

        blocked = False
        while x >= 0 and x < width and y < height and not blocked:
            # Falling straight down
            if y + 1 >= height or board[y + 1][x] == EMPTY:
                y += 1
                continue

            # Falling to the left
            if x - 1 < 0 or board[y + 1][x - 1] == EMPTY:
                y += 1
                x -= 1
                continue

            # Falling to the right
            if x + 1 >= width or board[y + 1][x + 1] == EMPTY:
                y += 1
                x += 1
                continue

            blocked = True

        if blocked:
            board[y][x] = SAND
            nSand += 1
            if args.part == 2 and y == START_Y - min_y and x == START_X - min_x:
                done = True
        elif x < 0 or x >= width or y >= height:
            done = True

    # draw_board(board)

    print("Result:", nSand)


if __name__ == "__main__":
    main()
