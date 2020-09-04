from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
from math import sqrt
from typing import Dict, Iterator, List, Optional, Tuple, overload


class Status(int, Enum):
    SUSCEPTIBLE = auto()
    INFLECTED = auto()
    REMOVED = auto()


@dataclass
class Node:
    x: int
    y: int
    status: Status = Status.SUSCEPTIBLE
    density: float = 1


class Network:
    def __init__(self, height: int, width: int, default: Status = Status.SUSCEPTIBLE):
        self.height = height
        self.width = width
        self.grid: List[List[Node]] = []

        self.create(default)

    @property
    def status(self):
        stat: Dict[Status, List[Node]] = {}
        for i in self.all:
            stat[i.status] = stat.get(i.status, []) + [i]
        return stat

    @property
    def center(self):
        return self.get(self.width // 2, self.height // 2)

    @property
    def all(self) -> List[Node]:
        l = []
        for i in self.grid:
            l.extend(i)
        return l

    def create(self, default: Status = Status.SUSCEPTIBLE):
        self.grid.clear()
        self.grid.extend(
            [
                [Node(x=j, y=i, status=default) for j in range(self.width)]
                for i in range(self.height)
            ]
        )

    def get(self, x: int, y: int) -> Node:
        assert self.exist(x, y)
        return self.grid[y][x]

    def exist(self, x: int, y: int) -> bool:
        return (x >= 0 and y >= 0) and (x < self.width and y < self.height)

    @overload
    def nearby(self, *, node: Node, radius: int = 1) -> List[Node]:
        ...

    @overload
    def nearby(self, x: int, y: int, *, radius: int = 1) -> List[Node]:
        ...

    def nearby(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        *,
        node: Optional[Node] = None,
        radius: int = 1,
    ) -> List[Node]:
        if node is not None:
            x, y = node.x, node.y
        assert (x is not None) and (y is not None)
        squarePositions: List[Tuple[int, int]] = []
        for i in range(x - radius, x + radius + 1):
            squarePositions.extend([(i, j) for j in range(y - radius, y + radius + 1)])
        nodes: List[Node] = [
            node
            for node in (
                self.get(*position)
                for position in squarePositions
                if self.exist(*position)
            )
            if sqrt((x - node.x) ** 2 + (y - node.y) ** 2) <= radius
        ]
        return nodes

    def makeDensityDistribution(
        self, center: Tuple[int, int], *, density: int = 2, radius: int = 5
    ):
        x, y = center
        centerNode = self.get(x, y)
        centerNode.density = density
        attenuation = (density - 1) / radius
        for i in range(1, radius + 1):
            for node in self.nearby(x, y, radius=i):
                if node.density != 1:
                    continue
                node.density = density - (attenuation * i)
                if node.density <= 1:
                    node.density = 1
        return self

    def deepcopy(self):
        return deepcopy(self)

    def __repr__(self):
        # flake8:noqa:W503
        return (
            f"<{self.__class__.__name__} at 0x{id(self):x} "
            + f"with {self.width*self.height} nodes:"
            + "".join(("\n\t" + "\t".join(j.status.name for j in i)) for i in self.grid)
            + "\t>"
        )

    def __iter__(self) -> Iterator[Node]:
        return iter(self.all)
