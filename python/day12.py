from typing import Any, NamedTuple


class Region(NamedTuple):
    area: int
    presents: list[int]


def extract_shapes(chunks: list[str]) -> list[int]:
    shapes = []
    for chunk in chunks:
        count = sum(1 if char == "#" else 0 for char in chunk)
        shapes.append(count)
    return shapes


def extract_regions(chunk: str) -> list[Region]:
    regions = []
    for line in chunk.splitlines():
        dims_str, presents_str = line.split(": ")
        w, h = dims_str.split("x")
        region = Region(
            area=int(w) * int(h),
            presents=[int(n) for n in presents_str.split()],
        )
        regions.append(region)
    return regions


def run(text: str) -> tuple[Any, Any]:
    chunks = text.split("\n\n")
    shapes = extract_shapes(chunks[:-1])
    regions = extract_regions(chunks[-1])

    count = 0
    for region in regions:
        if region.area >= sum(n * 9 for n in region.presents):
            # The region is big enough to fit all presents fit even if we treat
            # them as 3x3 boxes.
            count += 1
        elif region.area < sum(n * s for n, s in zip(region.presents, shapes)):
            # The region is too small to fit all presents irrespective of how
            # they are oriented.
            pass
        else:
            # All regions are either obviously too small or obviously big
            # enough - no need to worry about packing.
            assert False

    return count, None
