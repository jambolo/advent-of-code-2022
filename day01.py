# Advent of Code 2022
# Day 1

from utils import setup, load


DAY = 1


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    # Sum the weights for each elf
    weights = []
    weight_sum = 0
    i = 0
    for line in lines:
        line = line.strip()
        if line:
            weight_sum += int(line)
        else:
            weights.append(weight_sum)
            #            print(f'Elf #{i} is carrying {weight_sum}')
            weight_sum = 0
            i = i + 1

    # Find the top three
    max1 = 0
    max2 = 0
    max3 = 0

    for weight in weights:
        if weight > max1:
            max3 = max2
            max2 = max1
            max1 = weight
        elif weight > max2:
            max3 = max2
            max2 = weight
        elif weight > max3:
            max3 = weight

    if args.part == 1:
        print(f"Result: {max1}")

    if args.part == 2:
        sum_of_top_3 = max1 + max2 + max3
        print(f"Result: {sum_of_top_3}")


if __name__ == "__main__":
    main()
