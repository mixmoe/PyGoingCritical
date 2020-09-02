# flake8:noqa:E501
from queue import Queue
from threading import Thread
from typing import Any, Callable, Dict, Iterator, Optional, Tuple

from PIL import Image, ImageColor
from PIL.Image import Image as ImageClass

from utils.misc import TimeIt

from .core import Network, Node, Status

SpreadModel_T = Callable[[Network], Iterator[Network]]
Render_T = Callable[[Network], Callable[..., ImageClass]]

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

    def rendBackground(self) -> ImageClass:
        height, width = self.network.height, self.network.width
        return Image.new(
            "RGBA",
            (
                height * (self.cellSize + self.gridSize) + self.gridSize,
                width * (self.cellSize + self.gridSize) + self.gridSize,
            ),
            self.gridColor,
        )

    def rendCell(self, cell: Node) -> Tuple[ImageClass, int, int]:
        x = cell.x * (self.cellSize + self.gridSize) + self.gridSize
        y = cell.y * (self.cellSize + self.gridSize) + self.gridSize
        r, g, b, *_ = ImageColor.getrgb(self.colorMap[cell.status])
        c = Image.new("RGBA", (self.cellSize, self.cellSize), (r, g, b, 0xBF))
        return c, x, y

    @TimeIt
    def __call__(self) -> ImageClass:
        background = self.rendBackground()
        for i in self.network.all:
            cell, x, y = self.rendCell(i)
            background.paste(cell, (x, y), cell)
        return background


class DensityRender(Render):
    def rendCell(self, cell: Node):
        assert cell.density >= 1 and cell.density <= 2
        x = cell.x * (self.cellSize + self.gridSize) + self.gridSize
        y = cell.y * (self.cellSize + self.gridSize) + self.gridSize
        r, g, b, *_ = ImageColor.getrgb(self.colorMap[cell.status])
        a = 0xBF + round((cell.density - 1) * 0x40)
        c = Image.new("RGBA", (self.cellSize, self.cellSize), (r, g, b, a))
        return c, x, y
