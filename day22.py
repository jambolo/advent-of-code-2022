# Advent of Code 2022
# Day 22

import copy
import re
from typing import Callable, Literal, NotRequired, TypedDict

from utils import load, setup


DAY = 22
NUMBER_OF_DIRECTIONS = 4
RIGHT = 0
DOWN = 1
LEFT = 2
UP = 3
INITIAL_DIRECTION = RIGHT

type Direction = Literal[0, 1, 2, 3]  # RIGHT, DOWN, LEFT, UP
type Turn = Literal["R", "L"]
type RouteStep = int | Turn
type Position = tuple[int, int]
type MoveResult = tuple[int, int, Direction]


class Map(TypedDict):
    tiles: list[str]
    width: int
    height: int
    row_extents: NotRequired[list[tuple[int, int]]]
    column_extents: NotRequired[list[tuple[int, int]]]
    start: NotRequired[Position]


MoveFn = Callable[[Map, int, int], MoveResult]


def replace_at_index(s: str, i: int, c: str) -> str:
    return s[:i] + c + s[i + len(c) :]


def parse_route(line: str) -> list[RouteStep]:
    i = 0
    route: list[RouteStep] = []
    while i < len(line):
        match = re.search(r"(\d+)|(R|L)", line[i:])
        assert match is not None
        token = match.group()
        if token == "R" or token == "L":
            route.append(token)
        else:
            route.append(int(token))
        i += match.span()[1]
    return route


def find_row_extents(world: Map) -> list[tuple[int, int]]:
    extents: list[tuple[int, int]] = []
    for row in world["tiles"]:
        extents.append((len(row) - len(row.lstrip()), len(row)))
    return extents


def find_column_extents(world: Map) -> list[tuple[int, int]]:
    extents: list[tuple[int, int]] = []
    for c in range(world["width"]):
        start = 0
        end = world["height"]
        for r in range(world["height"]):
            if c < len(world["tiles"][r]) and world["tiles"][r][c] != " ":
                start = r
                break
        for r in range(start + 1, world["height"]):
            if c >= len(world["tiles"][r]) or world["tiles"][r][c] == " ":
                end = r
                break
        extents.append((start, end))
    return extents


def find_blocks(world: Map) -> None:
    blocks: list[list[int]] = []
    for r in range(world["height"]):
        row = world["tiles"][r]
        row_blocks = []
        for c in range(world["row_extents"][r][0], world["row_extents"][r][1]):
            if row[c] == "#":
                row_blocks.append(c)
        blocks.append(row_blocks)


def print_map(world: Map) -> None:
    for row in world["tiles"]:
        for c in row:
            print(c, end=" ")
        print("")


def print_annotated_map(world: Map, my_r: int, my_c: int, direction: Direction) -> None:
    tiles: list[str] = copy.deepcopy(world["tiles"])
    row_extents = world["row_extents"]
    column_extents = world["column_extents"]
    for r in range(world["height"]):
        row = tiles[r]
        if row[row_extents[r][0]] != "#":
            row = replace_at_index(row, row_extents[r][0], "|")
        if row[row_extents[r][1] - 1] != "#":
            row = replace_at_index(row, row_extents[r][1] - 1, "|")
        for c in range(row_extents[r][0], row_extents[r][1]):
            if (r == column_extents[c][0] or r == column_extents[c][1] - 1) and row[c] != "#":
                row = replace_at_index(row, c, "-")
        tiles[r] = row
        if r == world["start"][0]:
            tiles[r] = replace_at_index(tiles[r], world["start"][1], "A")
        if r == my_r:
            tiles[r] = replace_at_index(tiles[r], my_c, ">v<^"[direction])

    annotated: Map = {"tiles": tiles, "width": world["width"], "height": world["height"]}
    print_map(annotated)


def wrap_right(r: int, c: int) -> MoveResult:
    match r // 50:
        case 0:  # 0 -> 3
            return (49 - (r - 0) + 100, 49 - ((c - 100) - 50) + 50, LEFT)
        case 1:  # 2 -> 0
            return (49 - ((c - 50) - 50) + 0, (r - 50) + 100, UP)
        case 2:  # 3 -> 0
            return (49 - (r - 100) + 0, 49 - ((c - 50) - 50) + 100, LEFT)
        case 3:  # 5 -> 3
            return (49 - ((c - 0) - 50) + 100, (r - 150) + 50, UP)
        case _:
            raise Exception("invalid wrap row")


def wrap_down(r: int, c: int) -> MoveResult:
    match c // 50:
        case 0:  # 5 -> 0
            return (((r - 150) - 50) + 0, (c - 0) + 100, DOWN)
        case 1:  # 3 -> 5
            return ((c - 50) + 150, 49 - ((r - 100) - 50) + 0, LEFT)
        case 2:  # 0 -> 2
            return ((c - 100) + 50, 49 - ((r - 0) - 50) + 50, LEFT)
        case _:
            raise Exception("invalid wrap row")


def wrap_left(r: int, c: int) -> MoveResult:
    match r // 50:
        case 0:  # 1 -> 4
            return (49 - (r - 0) + 100, 49 - ((c - 50) + 50) + 0, RIGHT)
        case 1:  # 2 -> 4
            return (49 - ((c - 50) + 50) + 100, (r - 50) + 0, DOWN)
        case 2:  # 4 -> 1
            return (49 - (r - 100) + 0, 49 - ((c - 0) + 50) + 50, RIGHT)
        case 3:  # 5 -> 1
            return (49 - ((c - 0) + 50) + 0, (r - 150) + 50, DOWN)
        case _:
            raise Exception("invalid wrap row")


def wrap_up(r: int, c: int) -> MoveResult:
    match c // 50:
        case 0:  # 4 -> 2
            return ((c - 0) + 50, 49 - ((r - 100) + 50) + 50, RIGHT)
        case 1:  # 1 -> 5
            return ((c - 50) + 150, 49 - ((r - 0) + 50) + 0, RIGHT)
        case 2:  # 0 -> 5
            return (((r - 0) + 50) + 150, (c - 100) + 0, UP)
        case _:
            raise Exception("invalid wrap row")


def turn_right(direction: Direction) -> Direction:
    return (direction + 1) % NUMBER_OF_DIRECTIONS


def turn_left(direction: Direction) -> Direction:
    return (direction - 1) % NUMBER_OF_DIRECTIONS


def move_right_1(world: Map, r: int, c: int) -> MoveResult:
    d = RIGHT
    r1 = r
    c1 = c + 1
    d1 = d
    if c1 >= world["row_extents"][r1][1]:
        c1 = world["row_extents"][r1][0]
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_down_1(world: Map, r: int, c: int) -> MoveResult:
    d = DOWN
    r1 = r + 1
    c1 = c
    d1 = d
    if r1 >= world["column_extents"][c1][1]:
        r1 = world["column_extents"][c1][0]
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_left_1(world: Map, r: int, c: int) -> MoveResult:
    d = LEFT
    r1 = r
    c1 = c - 1
    d1 = d
    if c1 < world["row_extents"][r1][0]:
        c1 = world["row_extents"][r1][1] - 1
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_up_1(world: Map, r: int, c: int) -> MoveResult:
    d = UP
    r1 = r - 1
    c1 = c
    d1 = d
    if r1 < world["column_extents"][c1][0]:
        r1 = world["column_extents"][c1][1] - 1
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_right_2(world: Map, r: int, c: int) -> MoveResult:
    d = RIGHT
    r1 = r
    c1 = c + 1
    d1 = d
    if c1 >= world["row_extents"][r1][1]:
        (r1, c1, d1) = wrap_right(r1, c1)
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_down_2(world: Map, r: int, c: int) -> MoveResult:
    d = DOWN
    r1 = r + 1
    c1 = c
    d1 = d
    if r1 >= world["column_extents"][c1][1]:
        (r1, c1, d1) = wrap_down(r1, c1)
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_left_2(world: Map, r: int, c: int) -> MoveResult:
    d = LEFT
    r1 = r
    c1 = c - 1
    d1 = d
    if c1 < world["row_extents"][r1][0]:
        (r1, c1, d1) = wrap_left(r1, c1)
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def move_up_2(world: Map, r: int, c: int) -> MoveResult:
    d = UP
    r1 = r - 1
    c1 = c
    d1 = d
    if r1 < world["column_extents"][c1][0]:
        (r1, c1, d1) = wrap_up(r1, c1)
    if world["tiles"][r1][c1] != "#":
        return (r1, c1, d1)
    else:
        return (r, c, d)


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    lines: list[str] = load.lines(args.input)

    world: Map
    tiles: list[str] = []
    i = 0
    width = 0
    while lines[i].rstrip():
        line = lines[i].rstrip()
        tiles.append(line)
        if len(line) > width:
            width = len(line)
        i += 1
    height = len(tiles)

    world = {"tiles": tiles, "width": width, "height": height}

    i += 1  # skip the blank line

    route: list[RouteStep] = parse_route(lines[i].rstrip())

    start = len(world["tiles"][0]) - len(world["tiles"][0].lstrip())
    world["start"] = (0, start)

    # Analysis

    world["row_extents"] = find_row_extents(world)
    world["column_extents"] = find_column_extents(world)

    if args.part == 1:
        move_right: MoveFn = move_right_1
        move_down: MoveFn = move_down_1
        move_left: MoveFn = move_left_1
        move_up: MoveFn = move_up_1
    if args.part == 2:
        move_right = move_right_2
        move_down = move_down_2
        move_left = move_left_2
        move_up = move_up_2
    r = 0
    c = start
    direction: Direction = INITIAL_DIRECTION
    for step in route:
        if isinstance(step, int):
            for i in range(step):
                match direction:
                    case 0:  # right
                        (r, c, direction) = move_right(world, r, c)
                    case 1:  # down
                        (r, c, direction) = move_down(world, r, c)
                    case 2:  # left
                        (r, c, direction) = move_left(world, r, c)
                    case 3:  # up
                        (r, c, direction) = move_up(world, r, c)
                    case _:
                        raise Exception("invalid direction")
        elif isinstance(step, str):
            if step == "R":
                direction = turn_right(direction)
            elif step == "L":
                direction = turn_left(direction)
            else:
                raise Exception("invalid turn")

    password = 1000 * (r + 1) + 4 * (c + 1) + direction
    print("Result:", password)


if __name__ == "__main__":
    main()
