# Advent of Code 2022
# Day 6

from utils import setup, load


DAY = 6


def print_marker(buffer: list[str], i: int) -> None:
    s = "|"
    if i > 0:
        s += "".join(buffer[i:])
        s += "".join(buffer[:i])
    else:
        s += "".join(buffer)
    s += "|"
    print(s)


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    if args.part == 1:
        marker_size = 4

    if args.part == 2:
        marker_size = 14

    data = load.string(args.input)

    buffer = []
    for i in range(marker_size):
        buffer.append(" ")

    i = 0
    n_unique = 0
    for c in data:
        buffer[i % marker_size] = c
        n_unique = n_unique + 1

        for j in range(1, n_unique):
            if c == buffer[(i - j + marker_size) % marker_size]:
                n_unique = j
                break
        if n_unique >= marker_size:
            i = i + 1
            break

        i = i + 1

    print(f"Result: {i}")


if __name__ == "__main__":
    main()
