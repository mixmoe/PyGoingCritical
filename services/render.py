# flake8:noqa:E501
from typing import Callable, Dict, Optional, Iterator

from PIL import Image, ImageColor

from utils.misc import TimeIt
from threading import Thread
from queue import Queue

from .core import Network, Status, Node

SpreadModel_T = Callable[[Network], Iterator[Network]]
Render_T = Callable[[Network, ...], Callable[..., Image]]  # type:ignore

COLOR_MAP = {
    Status.SUSCEPTIBLE: "#569AE2",
    Status.INFLECTED: "#FF7C7C",
    Status.REMOVED: "#9287E7",
}
CELL_SIZE = 20
GRID_SIZE = 2
GRID_COLOR = "#FFFFFF"


class Render:
    def __init__(
        self,
        network: Network,
        colorMap: Optional[Dict[Status, str]] = None,
        cellSize: Optional[int] = None,
        gridSize: Optional[int] = None,
        gridColor: Optional[str] = None,
    ):
        self.network = network.deepcopy()
        self.cellSize = cellSize or CELL_SIZE
        self.gridSize = gridSize or GRID_SIZE
        self.gridColor = gridColor or GRID_COLOR
        self.colorMap = colorMap or COLOR_MAP

    def rendBackground(self):
        height, width = self.network.height, self.network.width
        return Image.new(
            "RGB",
            (
                height * (self.cellSize + self.gridSize) + self.gridSize,
                width * (self.cellSize + self.gridSize) + self.gridSize,
            ),
            self.gridColor,
        )

    def rendCell(self, cell: Node):
        x = cell.x * self.cellSize + self.gridSize
        y = cell.y * self.cellSize + self.gridSize
        c = Image.new(
            "RGB",
            (self.cellSize, self.cellSize),
            ImageColor.getrgb(self.colorMap[cell.status]),
        )
        return c, x, y

    @TimeIt
    def __call__(self):
        background = self.rendBackground()
        for i in self.network.all:
            cell, x, y = self.rendCell(i)
            background.paste(cell, (x, y))
        return background


class DensityRender(Render):
    def rendCell(self, cell: Node):
        assert cell.density >= 1 and cell.density <= 2
        x = cell.x * self.cellSize + self.gridSize
        y = cell.y * self.cellSize + self.gridSize
        r, g, b = ImageColor.getrgb(self.colorMap[cell.status])  # type:ignore
        a = 0x80 + (cell.density - 1) * 0x80
        return Image.new("RGBA", (self.cellSize, self.cellSize), (r, g, b, a)), x, y


class Processor:
    def __init__(
        self, model: SpreadModel_T, render: Render_T, size: int, queueSize: int = 10
    ):
        self._frameQueue: Queue[Image] = Queue(queueSize)  # type:ignore
        self._size = size
        self.model = model
        self.render = render
        self.rendThread = Thread(target=self.rend)
        self.stopped = False

    def rend(self):
        network = Network(self._size, self._size)
        for i in self.model(network):
            if self.stopped:
                break
            self._frameQueue.put(self.render(i)())  # type:ignore
        self.stopped = True

    def start(self):
        self.rendThread.start()

    def stop(self):
        self.stopped = True

    def __iter__(self):
        return self

    def __next__(self) -> Image:
        if self.stopped and self._frameQueue.empty():
            raise StopIteration
        return self._frameQueue.get()  # type:ignore
