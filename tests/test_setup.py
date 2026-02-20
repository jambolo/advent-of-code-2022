import sys
from unittest.mock import patch

import pytest

from utils.setup import parse_command_line, print_banner


class TestParseCommandLine:
    def test_defaults(self):
        with patch.object(sys, "argv", ["prog"]):
            args = parse_command_line(1)
        assert args.input == "data/day01-input.txt"
        assert args.part == 1

    def test_default_input_zero_pads_day(self):
        with patch.object(sys, "argv", ["prog"]):
            args = parse_command_line(7)
        assert args.input == "data/day07-input.txt"

    def test_default_input_double_digit_day(self):
        with patch.object(sys, "argv", ["prog"]):
            args = parse_command_line(25)
        assert args.input == "data/day25-input.txt"

    def test_custom_input_short_flag(self):
        with patch.object(sys, "argv", ["prog", "-i", "my_input.txt"]):
            args = parse_command_line(1)
        assert args.input == "my_input.txt"

    def test_custom_input_long_flag(self):
        with patch.object(sys, "argv", ["prog", "--input", "my_input.txt"]):
            args = parse_command_line(1)
        assert args.input == "my_input.txt"

    def test_part_1(self):
        with patch.object(sys, "argv", ["prog", "-p", "1"]):
            args = parse_command_line(1)
        assert args.part == 1

    def test_part_2(self):
        with patch.object(sys, "argv", ["prog", "-p", "2"]):
            args = parse_command_line(1)
        assert args.part == 2

    def test_part_long_flag(self):
        with patch.object(sys, "argv", ["prog", "--part", "2"]):
            args = parse_command_line(1)
        assert args.part == 2

    def test_invalid_part_rejected(self):
        with patch.object(sys, "argv", ["prog", "-p", "3"]):
            with pytest.raises(SystemExit):
                parse_command_line(1)

    def test_both_flags(self):
        with patch.object(sys, "argv", ["prog", "-i", "test.txt", "-p", "2"]):
            args = parse_command_line(12)
        assert args.input == "test.txt"
        assert args.part == 2


class TestPrintBanner:
    def test_output(self, capsys):
        print_banner(1, 1)
        assert capsys.readouterr().out == "=== Day 1, part 1 ===\n"

    def test_part_2(self, capsys):
        print_banner(25, 2)
        assert capsys.readouterr().out == "=== Day 25, part 2 ===\n"
