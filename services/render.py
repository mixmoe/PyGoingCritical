from typing import Dict, Optional

from PIL import Image

from utils.misc import TimeIt

from .core import Network, Status

COLOR_MAP = {
    Status.SUSCEPTIBLE: "#EEEEEE",
    Status.INFLECTED: "#4488FF",
    Status.REMOVED: "#C5C5C5",
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
        self.colorMap = {
            k: Image.new("RGB", (self.cellSize, self.cellSize), v)
            for k, v in (colorMap or COLOR_MAP).items()
        }

    @TimeIt
    def __call__(self) -> Image:
        height, width = self.network.height, self.network.width
        background = Image.new(
            "RGB",
            (
                height * (self.cellSize + self.gridSize) + self.gridSize,
                width * (self.cellSize + self.gridSize) + self.gridSize,
            ),
            self.gridColor,
        )
        for i in self.network.all:
            cell = self.colorMap[i.status]
            background.paste(
                cell,
                (
                    i.x * self.cellSize + self.gridSize,
                    i.y * self.cellSize + self.gridSize,
                ),
            )
        return background  # type:ignore
