from typing import Any, NamedTuple


class Rotation(NamedTuple):
    step: int
    distance: int


def extract_rotations(text: str) -> list[Rotation]:
    rotations = []
    for line in text.splitlines():
        direction = line[0]
        distance = int(line[1:])
        match direction:
            case "L":
                rotation = Rotation(-1, -distance)
            case "R":
                rotation = Rotation(+1, +distance)
            case _:
                assert False
        rotations.append(rotation)
    return rotations


def run(text: str) -> tuple[Any, Any]:
    rotations = extract_rotations(text)

    position = 50
    count_land = 0
    for rotation in rotations:
        position += rotation.distance
        position %= 100
        if position == 0:
            count_land += 1

    position = 50
    count_pass = 0
    for rotation in rotations:
        for _ in range(0, rotation.distance, rotation.step):
            position += rotation.step
            position %= 100
            if position == 0:
                count_pass += 1

    return count_land, count_pass
