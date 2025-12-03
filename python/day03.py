from typing import Any, Iterator


def extract_banks(text: str) -> Iterator[list[int]]:
    for line in text.splitlines():
        yield [int(c) for c in line]


def calculate_max_joltage(bank: list[int], count: int) -> int:
    digits = [-1] * count
    index = -1

    for position in range(count):
        lo = index + 1
        hi = len(bank) - (count - position - 1)
        for i, battery in enumerate(bank[lo:hi], start=lo):
            if battery > digits[position]:
                digits[position] = battery
                index = i

    joltage = 0
    for digit in digits:
        joltage *= 10
        joltage += digit

    return joltage


def run(text: str) -> tuple[Any, Any]:
    total_2 = 0
    total_12 = 0

    for bank in extract_banks(text):
        total_2 += calculate_max_joltage(bank, 2)
        total_12 += calculate_max_joltage(bank, 12)

    return total_2, total_12
