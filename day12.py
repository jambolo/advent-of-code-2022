# Advent of Code 2022
# Day 12

from utils import setup, load, pathfinding


DAY = 12

WIDTH = 162  # 8 # 162
HEIGHT = 41  # 5 # 41
START = 3240  # 0 # 3240
END = 3377  # 21 # 3377
IMPASSABLE = float("inf")


def height(c: str) -> int:
    heights = "abcdefghijklmnopqrstuvwxyz"
    return heights.find(c)


def heuristic(s: int) -> int:
    sx = s % WIDTH
    sy = s // WIDTH
    ex = END % WIDTH
    ey = END // WIDTH
    return abs(ex - sx) + abs(ey - sy)


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    maze = []

    for line in lines:
        line = line.strip()
        maze.extend(line)

    if maze[START] != "S":
        raise Exception(f"Invalid START at {START}: {maze[START]} vs S.")
    maze[START] = "a"
    if maze[END] != "E":
        raise Exception(f"Invalid END at {END}: {maze[END]} vs E.")
    maze[END] = "z"
    maze = [height(c) for c in maze]

    def cost(a, b):
        if maze[b] - maze[a] <= 1:
            return 1
        return IMPASSABLE

    def neighbors_of(s):
        sx = s % WIDTH
        sy = s // WIDTH
        neighbors = []
        if sx - 1 >= 0:
            neighbors.append(s - 1)
        if sx + 1 < WIDTH:
            neighbors.append(s + 1)
        if sy - 1 >= 0:
            neighbors.append(s - WIDTH)
        if sy + 1 < HEIGHT:
            neighbors.append(s + WIDTH)
        return neighbors

    if args.part == 1:
        total_cost, path = pathfinding.a_star(START, END, neighbors_of, heuristic, cost)
        print("Result:", len(path) - 1)

    if args.part == 2:
        best_score = IMPASSABLE
        for i in range(len(maze)):
            if maze[i] == 0:
                total_cost, path = pathfinding.a_star(i, END, neighbors_of, heuristic, cost)
                if path:
                    if len(path) - 1 < best_score:
                        best_score = len(path) - 1
        print("Result:", best_score)


if __name__ == "__main__":
    main()
