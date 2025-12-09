import itertools
from typing import Any, NamedTuple


class Tile(NamedTuple):
    x: int
    y: int


class Edge(NamedTuple):
    xmin: int
    ymin: int
    xmax: int
    ymax: int


class Rectangle(NamedTuple):
    xmin: int
    ymin: int
    xmax: int
    ymax: int

    @property
    def area(self) -> int:
        return (1 + self.xmax - self.xmin) * (1 + self.ymax - self.ymin)

    def intersected_by(self, edge: Edge) -> bool:
        if edge.xmax <= self.xmin:
            return False
        if edge.xmin >= self.xmax:
            return False
        if edge.ymax <= self.ymin:
            return False
        if edge.ymin >= self.ymax:
            return False
        return True


def extract_tiles(text: str) -> list[Tile]:
    tiles = []
    for line in text.splitlines():
        x, y = line.split(",")
        tile = Tile(x=int(x), y=int(y))
        tiles.append(tile)
    return tiles


def run(text: str) -> tuple[Any, Any]:
    tiles = extract_tiles(text)

    rectangles = sorted(
        [
            Rectangle(
                xmin=min(a.x, b.x),
                ymin=min(a.y, b.y),
                xmax=max(a.x, b.x),
                ymax=max(a.y, b.y),
            )
            for a, b in itertools.combinations(tiles, 2)
        ],
        key=lambda rect: rect.area,
        reverse=True,
    )

    edges = []
    for i in range(len(tiles)):
        a = tiles[i]
        b = tiles[i - 1]
        edge = Edge(
            xmin=min(a.x, b.x),
            ymin=min(a.y, b.y),
            xmax=max(a.x, b.x),
            ymax=max(a.y, b.y),
        )
        edges.append(edge)

    area1 = rectangles[0].area
    for rect in rectangles:
        if not any(rect.intersected_by(edge) for edge in edges):
            area2 = rect.area
            break
    else:
        assert False

    return area1, area2
