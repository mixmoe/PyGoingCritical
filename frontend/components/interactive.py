import tkinter as tk
from typing import Tuple

from PIL import Image, ImageTk


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
    def __init__(self, root: tk.Widget):
        super().__init__(root)
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
        ...

    def imagePlayControl(self):
        ...

    def imageReset(self):
        ...


class AdjustLayerRoot(tk.Frame):
    def __init__(
        self,
        root: tk.Widget,
        *,
        enableRecovery: bool = False,
        enableDensity: bool = False
    ):
        super().__init__(root)

        self.transmissionRateText = tk.Label(master=self, text="传染率")
        self.transmissionRateAdjuster = tk.Scale(
            master=self,
            from_=0,
            to=100,
            resolution=1,
            tickinterval=20,
            orient=tk.VERTICAL,
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
        )
        self.withDensityText = tk.Label(master=self, text="使用人口分布")
        self.withDensityCheckbox = tk.Checkbutton(
            master=self, state=tk.NORMAL if enableDensity else tk.DISABLED
        )

        self.transmissionRateText.grid(column=0, row=0, sticky=tk.S)
        self.transmissionRateAdjuster.grid(column=0, row=1, sticky=tk.N)
        self.recoveryRateText.grid(column=1, row=0, sticky=tk.S)
        self.recoveryRateAdjuster.grid(column=1, row=1, sticky=tk.N)
        self.withDensityText.grid(column=2, row=0, sticky=tk.S)
        self.withDensityCheckbox.grid(column=2, row=1, sticky=tk.N)


class InteractiveRoot(tk.Frame):
    def __init__(self, root: tk.Widget):
        super().__init__(root)
        self.imageView = ImageView(root=self, imageSize=(400, 400))
        self.buttons = ButtonsLayerRoot(root=self)
        self.adjust = AdjustLayerRoot(root=self)

        self.imageView.grid(column=0, row=0)
        self.buttons.grid(column=0, row=1)
        self.adjust.grid(column=0, row=2)
