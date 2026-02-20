# Advent of Code 2022
# Day 17

from utils import setup, load


DAY = 17
BOARD_WIDTH = 7

type Rock = dict[str, list[list[int]]]
type Board = list[list[int]]
type Signature = tuple[int, int, tuple[tuple[int, ...], ...]]

# Rock shapes.
# Note: the shapes are defined with the bottom row first
ROCKS: list[Rock] = [
    {"width": 4, "height": 1, "shape": [[1, 1, 1, 1]]},
    {"width": 3, "height": 3, "shape": [[0, 1, 0], [1, 1, 1], [0, 1, 0]]},
    {"width": 3, "height": 3, "shape": [[1, 1, 1], [0, 0, 1], [0, 0, 1]]},
    {"width": 1, "height": 4, "shape": [[1], [1], [1], [1]]},
    {"width": 2, "height": 2, "shape": [[1, 1], [1, 1]]},
]


def collision(board: Board, rock: Rock, bottom: int, left: int) -> bool:
    if bottom < 0 or left < 0 or left + rock["width"] > BOARD_WIDTH:
        return True

    for y in range(min(rock["height"], len(board) - bottom)):
        for x in range(rock["width"]):
            if board[bottom + y][left + x] == 1 and rock["shape"][y][x] == 1:
                return True
    return False


def draw_rock_on_board(board: Board, rock: Rock, bottom: int, left: int) -> None:
    w: int = rock["width"]
    h: int = rock["height"]
    if h + bottom > len(board):
        raise Exception("bad rock placement")
    for y in range(h):
        for x in range(w):
            if rock["shape"][y][x] == 1:
                board[bottom + y][left + x] = 1


class CycleDetector:
    def __init__(self, max_rounds: int) -> None:
        self.MAX_ROUNDS: int = max_rounds
        self.SIGNATURE_HEIGHT: int = 8
        self.rounds: dict[Signature, int] = {}
        self.heights: list[int] = []
        self.skipped_rounds: int | None = None
        self.skipped_rows: int | None = None

    def _generate_signature(self, jet: int, rock: int, board: Board, height: int) -> Signature:
        signature: Signature = (
            rock,
            jet,
            tuple(tuple(board[height - 1 - i]) for i in range(self.SIGNATURE_HEIGHT)),
        )
        return signature

    def detect_cycle(self, jet: int, rock: int, board: Board, height: int, i: int) -> bool:
        """Must be called at the beginning of each round until a cycle is detected. Returns True if a cycle is detected."""

        # If the height is less than the signature height, a signature cannot be generated, so store the height and return False.
        if height < self.SIGNATURE_HEIGHT:
            self.heights.append(height)
            return False

        # Generate the signature for this round and check if a round with the same signature has been seen before.
        signature = self._generate_signature(jet, rock, board, height)
        if signature in self.rounds:
            round_cycle_start: int = self.rounds[signature]  # Get the index of the first round of the cycle
            height_cycle_start: int = self.heights[round_cycle_start]  # Get the height at the start of the cycle
            round_cycle_length: int = i - round_cycle_start
            height_cycle_length: int = height - height_cycle_start
            rounds_remaining: int = self.MAX_ROUNDS - i
            full_cycles_remaining: int = rounds_remaining // round_cycle_length
            self.skipped_rounds: int = full_cycles_remaining * round_cycle_length
            self.skipped_rows: int = full_cycles_remaining * height_cycle_length
            return True
        else:
            self.rounds[signature] = i
            self.heights.append(height)
            return False

    def get_skips(self) -> tuple[int, int]:
        """Called after a cycle is detected to return how many rounds and rows should be skipped."""
        if self.skipped_rows is None or self.skipped_rounds is None:
            raise Exception("Skips not set")
        return self.skipped_rows, self.skipped_rounds


def main() -> None:
    args = setup.parse_command_line(DAY)
    setup.print_banner(DAY, args.part)

    # Read the file.
    jets: str = load.string(args.input)

    if args.part == 1:
        MAX_ROUNDS: int = 2022

    if args.part == 2:
        MAX_ROUNDS = 1000000000000

    board: Board = []  # The bottom row is index 0, the top row is index len(board) - 1
    jet: int = 0  # The index of the next jet to apply
    cycle_detector: CycleDetector = CycleDetector(MAX_ROUNDS)
    cycle_detected: bool = False
    skipped_rows: int = 0

    i: int = 0
    while i < MAX_ROUNDS:
        rock: int = i % len(ROCKS)
        height: int = len(board)  # Maximum height of the rocks

        # Check for cycles until one is found
        if not cycle_detected:
            cycle_detected = cycle_detector.detect_cycle(jet, rock, board, height, i)
            if cycle_detected:
                skipped_rows, skipped_rounds = cycle_detector.get_skips()
                i += skipped_rounds

        # Apply the jets and gravity to the current rock until it comes to rest
        shape: Rock = ROCKS[rock]
        bottom, left = height + 3, 2  # Starting position of the rock
        stopped: bool = False
        while not stopped:
            # Apply the jet
            direction: str = jets[jet]
            jet = (jet + 1) % len(jets)
            if direction == "<":
                if not collision(board, shape, bottom, left - 1):
                    left = left - 1
            elif direction == ">":
                if not collision(board, shape, bottom, left + 1):
                    left = left + 1
            else:
                raise Exception(f"Invalid jet: {direction}")

            # Fall one space
            if not collision(board, shape, bottom - 1, left):
                bottom = bottom - 1
            else:
                stopped = True

        # Add the rock to the board, first adding empty rows if the rock is above the current height of the board
        for _ in range((bottom + shape["height"] - len(board))):
            board.append([0, 0, 0, 0, 0, 0, 0])
        draw_rock_on_board(board, shape, bottom, left)
        i += 1

    print("Result", len(board) + skipped_rows)


if __name__ == "__main__":
    main()
