from copy import deepcopy
from dataclasses import dataclass
from enum import Enum, auto
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
    density: int = 1


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
        assert x >= 0 and y >= 0
        assert x < self.width and y < self.height
        return self.grid[y][x]

    @overload
    def nearby(self, *, node: Node) -> List[Node]:
        ...

    @overload
    def nearby(self, x: int, y: int) -> List[Node]:
        ...

    def nearby(
        self,
        x: Optional[int] = None,
        y: Optional[int] = None,
        *,
        node: Optional[Node] = None,
    ) -> List[Node]:
        if node is not None:
            x, y = node.x, node.y
        assert (x is not None) and (y is not None)
        positions: List[Tuple[int, int]] = [
            (x, y),
            (x - 1, y),
            (x + 1, y),
            (x, y - 1),
            (x, y + 1),
        ]
        nodes: List[Node] = []
        for x, y in positions:
            try:
                nodes.append(self.get(x, y))
            except AssertionError:
                pass
        return nodes
    
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
        for i in self.all:
            yield i
