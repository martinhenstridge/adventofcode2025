from typing import Any

import numpy as np
from scipy.optimize import linprog


def parse_indicators(raw: str) -> list[int]:
    return [i for i, char in enumerate(raw.strip("[]")) if char == "#"]


def parse_buttons(raw: str) -> list[list[int]]:
    return [[int(n) for n in b.strip("()").split(",")] for b in raw.split()]


def parse_joltages(raw: str) -> list[int]:
    return [int(num) for num in raw.strip("{}").split(",")]


def as_bitmask(indices: list[int]) -> int:
    mask = 0
    for index in indices:
        mask |= 1 << index
    return mask


def solve_indicators(buttons: list[list[int]], indicators: list[int]) -> int:
    indicators_bitmask = as_bitmask(indicators)
    button_bitmasks = [as_bitmask(button) for button in buttons]

    states = {0}
    count = 0
    while indicators_bitmask not in states:
        count += 1
        states_next = set()
        for state in states:
            for button in button_bitmasks:
                states_next.add(state ^ button)
        states = states_next
    return count


def solve_joltages(buttons: list[list[int]], joltages: list[int]) -> int:
    A = np.array(
        [[int(i in button) for button in buttons] for i, _ in enumerate(joltages)],
        dtype=int,
    )
    b = np.array(joltages, dtype=int)
    c = np.ones(len(buttons), dtype=int)

    result = linprog(
        c,
        A_eq=A,
        b_eq=b,
        integrality=1,
    )
    return round(result.fun)


def run(text: str) -> tuple[Any, Any]:
    total_indicators = 0
    total_joltages = 0

    for line in text.splitlines():
        raw_indicators, rest = line.split(maxsplit=1)
        raw_buttons, raw_joltages = rest.rsplit(maxsplit=1)

        indicators = parse_indicators(raw_indicators)
        buttons = parse_buttons(raw_buttons)
        joltages = parse_joltages(raw_joltages)

        total_indicators += solve_indicators(buttons, indicators)
        total_joltages += solve_joltages(buttons, joltages)

    return total_indicators, total_joltages
