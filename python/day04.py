from functools import cache
from typing import Any


def extract_grid(text: str) -> set[complex]:
    grid = set()
    for i, line in enumerate(text.splitlines()):
        for j, char in enumerate(line):
            if char == "@":
                p = complex(i, j)
                grid.add(p)
    return grid


@cache
def get_neighbours(p: complex) -> set[complex]:
    return {
        complex(p.real + dr, p.imag + dc)
        for dr in range(-1, +2)
        for dc in range(-1, +2)
        if not (dr == 0 and dc == 0)
    }


def run(text: str) -> tuple[Any, Any]:
    grid = extract_grid(text)

    count_accessible = 0
    for p in grid:
        if len(get_neighbours(p) & grid) < 4:
            count_accessible += 1

    count_removable = 0
    while True:
        removals = set()
        for p in grid:
            if len(get_neighbours(p) & grid) < 4:
                removals.add(p)
        if not removals:
            break
        grid -= removals
        count_removable += len(removals)

    return count_accessible, count_removable
