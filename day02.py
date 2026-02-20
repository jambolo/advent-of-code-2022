# Advent of Code 2022
# Day 2

from utils import setup, load


DAY = 2

ROCK = 1
PAPER = 2
SCISSORS = 3

WIN = 6
DRAW = 3
LOSS = 0

abc_map = {"A": ROCK, "B": PAPER, "C": SCISSORS}

xyz_map_1 = {"X": ROCK, "Y": PAPER, "Z": SCISSORS}

xyz_map_2 = {"X": LOSS, "Y": DRAW, "Z": WIN}

outcomes = [
    {"me": ROCK, "them": ROCK, "outcome": DRAW},
    {"me": ROCK, "them": PAPER, "outcome": LOSS},
    {"me": ROCK, "them": SCISSORS, "outcome": WIN},
    {"me": PAPER, "them": ROCK, "outcome": WIN},
    {"me": PAPER, "them": PAPER, "outcome": DRAW},
    {"me": PAPER, "them": SCISSORS, "outcome": LOSS},
    {"me": SCISSORS, "them": ROCK, "outcome": LOSS},
    {"me": SCISSORS, "them": PAPER, "outcome": WIN},
    {"me": SCISSORS, "them": SCISSORS, "outcome": DRAW},
]


def parse_line_1(line: str) -> list[int]:
    line = line.strip()
    moves = line.split()
    theirs = abc_map[moves[0]]
    mine = xyz_map_1[moves[1]]
    return [theirs, mine]


def parse_line_2(line: str) -> list[int]:
    line = line.strip()
    moves = line.split()
    theirs = abc_map[moves[0]]
    outcome = xyz_map_2[moves[1]]
    return [theirs, outcome]


def outcome(me: int, them: int) -> int:
    for o in outcomes:
        if me == o["me"] and them == o["them"]:
            return o["outcome"]
    raise Exception("outcome: invalid parameters.")


def choose_my_move(them: int, outcome: int) -> int:
    for o in outcomes:
        if them == o["them"] and outcome == o["outcome"]:
            return o["me"]
    raise Exception("choose_my_move: invalid parameters.")


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file
    lines = load.lines(args.input)

    my_final = 0
    their_final = 0
    for line in lines:
        if args.part == 1:
            [theirMove, myMove] = parse_line_1(line)
            myOutcome = outcome(myMove, theirMove)
            theirOutcome = outcome(theirMove, myMove)
        elif args.part == 2:
            [theirMove, myOutcome] = parse_line_2(line)
            myMove = choose_my_move(theirMove, myOutcome)
            theirOutcome = outcome(theirMove, myMove)
        else:
            raise Exception("Invalid args.part value")

        round_dict = {
            "mine": myMove,
            "theirs": theirMove,
            "myScore": myMove + myOutcome,
            "theirScore": theirMove + theirOutcome,
        }
        my_final += round_dict["myScore"]
        their_final += round_dict["theirScore"]

    print(f"Result: {my_final}")


if __name__ == "__main__":
    main()
