import collections
from typing import Any


def run(text: str) -> tuple[Any, Any]:
    rows = text.splitlines()

    beams = {rows[0].index("S"): 1}
    splits = 0

    for row in rows[1:]:
        if "^" not in row:
            continue

        beams_next = collections.defaultdict(int)
        for index, timelines in beams.items():
            match row[index]:
                case ".":
                    beams_next[index] += timelines
                case "^":
                    splits += 1
                    beams_next[index - 1] += timelines
                    beams_next[index + 1] += timelines
        beams = beams_next

    return splits, sum(beams.values())
