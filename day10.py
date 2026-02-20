# Advent of Code 2022
# Day 10

from utils import setup, load


DAY = 10


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    def draw_pixel(old_x):
        nonlocal column
        nonlocal row
        if old_x - 1 <= column and column <= old_x + 1:
            row += "#"
        else:
            row += " "
        column += 1
        # Draw the row
        if len(row) == 40:
            print(row)
            row = ""
            column = 0

    # Read the file
    lines = load.lines(args.input)

    cycle = 1
    x = 1
    epoch = 0
    strength_sum = 0
    row = ""
    column = 0

    if args.part == 1:
        for line in lines:
            line = line.strip()

            old_x = x

            # Execute
            opcode = line[:4]
            if opcode == "noop":
                cycle += 1
            elif opcode == "addx":
                operand = int(line[5:])
                x += operand
                cycle += 2
            else:
                raise Exception("Unknown opcode: " + opcode)

            # Detect new epoch
            if (cycle + 19) // 40 > epoch:
                epoch += 1
                strength = old_x * (epoch * 40 - 20)
                strength_sum += strength

        print(f"Result: {strength_sum}")

    if args.part == 2:
        print("Result:")
        for line in lines:
            line = line.strip()

            old_x = x

            # Execute
            opcode = line[:4]
            if opcode == "noop":
                draw_pixel(old_x)
                cycle += 1
            elif opcode == "addx":
                draw_pixel(old_x)
                draw_pixel(old_x)
                operand = int(line[5:])
                x += operand
                cycle += 2
            else:
                raise Exception("Unknown opcode: " + opcode)


if __name__ == "__main__":
    main()
