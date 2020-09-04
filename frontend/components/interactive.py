import tkinter as tk
from typing import Tuple

from PIL import Image, ImageTk
from ..bus import EventBus


class ImageView(tk.Frame):
    def __init__(self, root: tk.Frame, imageSize: Tuple[int, int]) -> None:
        super().__init__(root)
        self.image = Image.new("RGB", imageSize, (0xFF, 0xFF, 0xFF))
        self.imageSize = imageSize
        self.imageTk = ImageTk.PhotoImage(image=self.image, size=self.imageSize)
        self.imageLabel = tk.Label(
            master=self,
            image=self.imageTk,  # type:ignore
        )
        self.imageLabel.grid(column=0, row=0)

    def setImage(self, image: Image.Image):
        self.image = image.resize(self.imageSize)
        self.imageTk = ImageTk.PhotoImage(image=self.image, size=self.imageSize)
        self.imageLabel.configure(image=self.imageTk)  # type:ignore
        self.update()


class ButtonsLayerRoot(tk.Frame):
    def __init__(self, root: tk.Widget, *, name: str):
        super().__init__(root)
        self.widgetName = name
        self.stepButton = tk.Button(master=self, text="步进", command=self.imageStep)
        self.playControlButton = tk.Button(
            master=self, text="开始", command=self.imagePlayControl
        )
        self.resetButton = tk.Button(master=self, text="重置", command=self.imageReset)

        self.stepButton.grid(column=0, row=0)
        self.playControlButton.grid(column=1, row=0)
        self.resetButton.grid(column=2, row=0)

        self.paused = True

    def imageStep(self):
        EventBus.broadcast(f"{self.widgetName}_step", self)

    def imagePlayControl(self):
        EventBus.broadcast(f"{self.widgetName}_play_control", self)

    def imageReset(self):
        EventBus.broadcast(f"{self.widgetName}_reset", self)


class AdjustLayerRoot(tk.Frame):
    def __init__(
        self,
        root: tk.Widget,
        *,
        name: str,
        enableRecovery: bool = False,
        enableDensity: bool = False,
    ):
        super().__init__(root)
        self.widgetName = name
        self.transmissionRateText = tk.Label(master=self, text="传染率")
        self.transmissionRateAdjuster = tk.Scale(
            master=self,
            from_=0,
            to=100,
            resolution=1,
            tickinterval=20,
            orient=tk.VERTICAL,
            command=lambda *_: self.transmissionRateAdjust(),
        )
        self.recoveryRateText = tk.Label(master=self, text="康复率")
        self.recoveryRateAdjuster = tk.Scale(
            master=self,
            from_=0,
            to=100,
            resolution=1,
            tickinterval=20,
            orient=tk.VERTICAL,
            state=tk.NORMAL if enableRecovery else tk.DISABLED,
            command=lambda *_: self.recoveryRateAdjust(),
        )
        self.withDensityText = tk.Label(master=self, text="使用人口分布")
        self.withDensityCheckbox = tk.Checkbutton(
            master=self,
            state=tk.NORMAL if enableDensity else tk.DISABLED,
            command=self.densityStatusSwitch,
        )

        self.transmissionRateText.grid(column=0, row=0, sticky=tk.S)
        self.transmissionRateAdjuster.grid(
            column=0,
            row=1,
            sticky=tk.N,
        )
        self.recoveryRateText.grid(column=1, row=0, sticky=tk.S)
        self.recoveryRateAdjuster.grid(column=1, row=1, sticky=tk.N)
        self.withDensityText.grid(column=2, row=0, sticky=tk.S)
        self.withDensityCheckbox.grid(column=2, row=1, sticky=tk.N)

    def transmissionRateAdjust(self):
        EventBus.broadcast(f"{self.widgetName}_transmission_adjust", self)

    def recoveryRateAdjust(self):
        EventBus.broadcast(f"{self.widgetName}_recovery_adjust", self)

    def densityStatusSwitch(self):
        EventBus.broadcast(f"{self.widgetName}_density_switch", self)


class InteractiveRoot(tk.Frame):
    def __init__(
        self,
        root: tk.Widget,
        *,
        name: str,
        enableRecovery: bool = False,
        enableDensity: bool = False,
    ):
        super().__init__(root)
        self.widgetName = name
        self.imageView = ImageView(root=self, imageSize=(400, 400))
        self.buttons = ButtonsLayerRoot(root=self, name=name)
        self.adjust = AdjustLayerRoot(
            root=self,
            name=name,
            enableRecovery=enableRecovery,
            enableDensity=enableDensity,
        )

        self.imageView.grid(column=0, row=0)
        self.buttons.grid(column=0, row=1)
        self.adjust.grid(column=0, row=2)

        EventBus.broadcast(f"{name}_init", self)
