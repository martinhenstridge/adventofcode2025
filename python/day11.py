import functools
from typing import Any


def parse_graph(text: str) -> dict[str, list[str]]:
    graph = {}
    for line in text.splitlines():
        device, outputs = line.split(": ")
        graph[device] = outputs.split()
    return graph


def run(text: str) -> tuple[Any, Any]:
    graph = parse_graph(text)

    @functools.cache
    def count_paths(goal: str, node: str) -> int:
        if node == goal:
            return 1
        if node not in graph:
            return 0
        return sum(count_paths(goal, output) for output in graph[node])

    # you -> out
    count_you_out = count_paths(goal="out", node="you")

    # svr -> dac -> fft -> out
    count_svr_dac = count_paths(goal="dac", node="svr")
    count_dac_fft = count_paths(goal="fft", node="dac")
    count_fft_out = count_paths(goal="out", node="fft")

    # svr -> fft -> dac -> out
    count_svr_fft = count_paths(goal="fft", node="svr")
    count_fft_dac = count_paths(goal="dac", node="fft")
    count_dac_out = count_paths(goal="out", node="dac")

    # svr -> out
    count_via_dac_fft = count_svr_dac * count_dac_fft * count_fft_out
    count_via_fft_dac = count_svr_fft * count_fft_dac * count_dac_out
    count_svr_out = count_via_dac_fft + count_via_fft_dac

    return count_you_out, count_svr_out
