from typing import Any, Iterator, NamedTuple


class Rotation(NamedTuple):
    step: int
    distance: int


def extract_rotations(text: str) -> Iterator[Rotation]:
    for line in text.splitlines():
        direction = line[0]
        distance = int(line[1:])
        match direction:
            case "L":
                yield Rotation(-1, -distance)
            case "R":
                yield Rotation(+1, +distance)
            case _:
                assert False


def run(text: str) -> tuple[Any, Any]:
    position = 50
    count_land = 0
    count_pass = 0

    for rotation in extract_rotations(text):
        for _ in range(0, rotation.distance, rotation.step):
            position += rotation.step
            position %= 100
            if position == 0:
                count_pass += 1
        if position == 0:
            count_land += 1

    return count_land, count_pass
