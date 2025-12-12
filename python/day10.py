from typing import Any


def parse_indicator(raw: str) -> int:
    lights = 0
    for i, char in enumerate(raw[1:-1]):
        if char == "#":
            lights |= 1 << i
    return lights


def parse_buttons(raw: str) -> list[int]:
    buttons = []
    for part in raw.split():
        button = 0
        for wires in part[1:-1].split(","):
            for wire in wires:
                button |= 1 << int(wire)
        buttons.append(button)
    return buttons


def parse_joltages(raw: str) -> list[int]:
    return [int(num) for num in raw[1:-1].split(",")]


def run(text: str) -> tuple[Any, Any]:
    # text = TEXT
    total = 0
    for line in text.splitlines():
        raw_indicator, rest = line.split(maxsplit=1)
        raw_buttons, raw_joltages = rest.rsplit(maxsplit=1)

        indicator = parse_indicator(raw_indicator)
        buttons = parse_buttons(raw_buttons)
        joltages = parse_joltages(raw_joltages)

        states = {0}
        count = 0
        while indicator not in states:
            count += 1
            states_next = set()
            for state in states:
                for button in buttons:
                    states_next.add(state ^ button)
            states = states_next
        total += count

    return total, None


TEXT = """\
[.##.] (3) (1,3) (2) (2,3) (0,2) (0,1) {3,5,4,7}
[...#.] (0,2,3,4) (2,3) (0,4) (0,1,2) (1,2,3,4) {7,5,12,7,2}
[.###.#] (0,1,2,3,4) (0,3,4) (0,1,2,4,5) (1,2) {10,11,11,5,10,5}
"""
