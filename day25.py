# Advent of Code 2022
# Day 25

from utils import setup, load


DAY = 25


def to_int(s: str) -> int:
    n = 0
    for c in s:
        n = n * 5 + ("=-012".index(c) - 2)
    return n


def to_snafu(n: int) -> str:
    s = ""
    if n == 0:
        s = "0"
    while n != 0:
        n += 2
        s = "=-012"[n % 5] + s
        n = n // 5
    return s


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    lines = load.lines(args.input)

    numbers = [to_int(line.rstrip()) for line in lines]

    total_sum = 0
    for n in numbers:
        total_sum += n

    if args.part == 1:
        print("Result:", to_snafu(total_sum))


if __name__ == "__main__":
    main()
