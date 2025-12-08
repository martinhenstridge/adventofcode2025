import itertools
from typing import Any, NamedTuple


class Box(NamedTuple):
    x: int
    y: int
    z: int


def extract_boxes(text: str) -> list[Box]:
    return [Box(*map(int, line.split(","))) for line in text.splitlines()]


def dist2(pair: tuple[Box, Box]) -> int:
    return (
        (pair[0].x - pair[1].x) ** 2
        + (pair[0].y - pair[1].y) ** 2
        + (pair[0].z - pair[1].z) ** 2
    )


def run(text: str) -> tuple[Any, Any]:
    boxes = extract_boxes(text)

    circuits = {box: {box} for box in boxes}
    pairs = sorted(itertools.combinations(boxes, 2), key=dist2)

    for a, b in pairs[:1000]:
        combined = circuits[a] | circuits[b]
        for box in combined:
            circuits[box] = combined
    unique = {id(c): c for c in circuits.values()}
    largest = sorted(unique.values(), key=len, reverse=True)
    product1 = len(largest[0]) * len(largest[1]) * len(largest[2])

    product2 = 1
    for a, b in pairs[1000:]:
        combined = circuits[a] | circuits[b]
        if len(combined) == len(boxes):
            product2 = a.x * b.x
            break
        for box in combined:
            circuits[box] = combined

    return product1, product2
