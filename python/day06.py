import functools
import itertools
import operator
from typing import Any, Iterator

OPERATIONS = {
    "+": operator.add,
    "*": operator.mul,
}


def extract_word_columns(text: str) -> Iterator[tuple[str, ...]]:
    rows = [line.split() for line in text.splitlines()]
    yield from zip(*rows)


def extract_char_columns(text: str) -> Iterator[tuple[str, ...]]:
    rows = text.splitlines()
    yield from zip(*rows)


def run(text: str) -> tuple[Any, Any]:
    total1 = 0
    for column in extract_word_columns(text):
        operation = OPERATIONS[column[-1]]
        operands = [int(n) for n in column[:-1]]
        total1 += functools.reduce(operation, operands)

    total2 = 0
    for line_is_empty, line_group in itertools.groupby(
        extract_char_columns(text),
        lambda line: all(char.isspace() for char in line),
    ):
        if line_is_empty:
            continue
        lines = list(line_group)
        operation = OPERATIONS[lines[0][-1]]
        operands = [int("".join(line[:-1])) for line in lines]
        total2 += functools.reduce(operation, operands)

    return total1, total2
