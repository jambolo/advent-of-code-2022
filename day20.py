# Advent of Code 2022
# Day 20

from utils import setup, load


DAY = 20


def move(data: list[dict[str, int]], src: int, count: int) -> None:
    element = data.pop(src)
    dst = src + count
    data.insert(dst % len(data), element)


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    if args.part == 1:
        NUMBER_OF_CYCLES = 1
    else:
        KEY = 811589153
        NUMBER_OF_CYCLES = 10

    # Read the file.
    lines = load.lines(args.input)

    original: list[int] = [int(line) for line in lines]
    size: int = len(original)

    if args.part == 2:
        original = [o * KEY for o in original]

    decrypted: list[dict[str, int]] = [{"value": o, "position": i} for i, o in enumerate(original)]

    for c in range(NUMBER_OF_CYCLES):
        for i in range(size):
            for k, d in enumerate(decrypted):
                if d["position"] == i:
                    v = d["value"]
                    if v != 0:  # if 0, don't move
                        move(decrypted, k, v)
                    break

    result: list[int] = [d["value"] for d in decrypted]

    at: int = result.index(0)
    x: int = result[(at + 1000) % size]
    y: int = result[(at + 2000) % size]
    z: int = result[(at + 3000) % size]

    print("Result:", x + y + z)


if __name__ == "__main__":
    main()
