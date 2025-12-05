from dataclasses import dataclass
from typing import Any, Iterator


@dataclass
class Range:
    lower: int
    upper: int

    def contains(self, value: int) -> bool:
        if value < self.lower:
            return False
        if value > self.upper:
            return False
        return True

    def overlaps(self, other: "Range") -> bool:
        assert self.lower <= other.lower
        return other.lower <= (self.upper + 1)

    def extend(self, other: "Range") -> None:
        self.lower = min(self.lower, other.lower)
        self.upper = max(self.upper, other.upper)

    def count(self) -> int:
        return 1 + self.upper - self.lower

    def __lt__(self, other: "Range") -> bool:
        return (self.lower, self.upper) < (other.lower, other.upper)


def extract_ranges(lines: Iterator[str]) -> list[Range]:
    ranges = []
    for line in lines:
        if not line:
            break
        lower, upper = line.split("-")
        r = Range(lower=int(lower), upper=int(upper))
        ranges.append(r)
    return ranges


def extract_available(lines: Iterator[str]) -> list[int]:
    return [int(line) for line in lines]


def combine_ranges(ranges: list[Range]) -> list[Range]:
    ranges.sort()
    combined = []
    idx = 0

    while idx < len(ranges):
        head = ranges[idx]
        idx += 1
        for candidate in ranges[idx:]:
            if not head.overlaps(candidate):
                break
            head.extend(candidate)
            idx += 1
        combined.append(head)

    return combined


def run(text: str) -> tuple[Any, Any]:
    lines = iter(text.splitlines())

    ranges = extract_ranges(lines)
    ranges = combine_ranges(ranges)
    available = extract_available(lines)

    count_available = sum(
        1 if any(r.contains(i) for r in ranges) else 0 for i in available
    )
    count_possible = sum(r.count() for r in ranges)

    return count_available, count_possible
