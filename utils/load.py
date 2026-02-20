# File loading utilities


def lines(name: str) -> list[str]:
    """Read all lines from a file with BOM-aware encoding."""
    with open(name, mode="r", encoding="utf-8-sig") as file:
        return file.readlines()


def string(name: str) -> str:
    """Read entire file into a string with BOM-aware encoding."""
    with open(name, mode="r", encoding="utf-8-sig") as file:
        return file.read().strip()
