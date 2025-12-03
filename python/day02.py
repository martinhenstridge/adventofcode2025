import re
from typing import Any, Iterator


def extract_pid_ranges(text: str) -> Iterator[tuple[int, int]]:
    for r in text.strip().split(","):
        a, b = r.split("-")
        yield int(a), int(b)


def run(text: str) -> tuple[Any, Any]:
    pattern_twice = re.compile(r"(\d+?)(\1)")
    pattern_multi = re.compile(r"(\d+?)(\1)+")

    total_twice = 0
    total_multi = 0

    for a, b in extract_pid_ranges(text):
        for n in range(a, b + 1):
            candidate = str(n)
            if pattern_multi.fullmatch(candidate):
                total_multi += n
                if pattern_twice.fullmatch(candidate):
                    total_twice += n

    return total_twice, total_multi
