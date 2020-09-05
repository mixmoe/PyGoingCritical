import tkinter as tk
from typing import Tuple

from PIL import Image, ImageTk

from ..bus import EventBusNamespace


class BusProvider:
    def __init__(self, name: str) -> None:
        self.rootComponent: "InteractiveRoot" = EventBusNamespace.get(name, "component")
        self.eventBus = EventBusNamespace.get(name)


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


class ButtonsLayerRoot(tk.Frame, BusProvider):
    def __init__(self, root: tk.Widget, *, name: str):
        tk.Frame.__init__(self, root)
        BusProvider.__init__(self, name)
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
        self.eventBus.broadcast("step", self.rootComponent)

    def imagePlayControl(self):
        self.eventBus.broadcast("play_control", self.rootComponent)

    def imageReset(self):
        self.eventBus.broadcast("reset", self.rootComponent)


class AdjustLayerRoot(tk.Frame, BusProvider):
    def __init__(
        self,
        root: tk.Widget,
        *,
        name: str,
        enableRecovery: bool = False,
        enableDensity: bool = False,
    ):
        tk.Frame.__init__(self, master=root)
        BusProvider.__init__(self, name=name)
        self.widgetName = name
        self.densityEnabled = tk.BooleanVar(master=self, value=False)
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
            variable=self.densityEnabled,
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

        if enableDensity:
            self.densityStatusSwitch()

    def transmissionRateAdjust(self):
        self.eventBus.broadcast("transmission_adjust", self.rootComponent)

    def recoveryRateAdjust(self):
        self.eventBus.broadcast("recovery_adjust", self.rootComponent)

    def densityStatusSwitch(self):
        self.eventBus.broadcast("density_switch", self.rootComponent)
        if self.densityEnabled.get():
            self.withDensityCheckbox.configure(text="启用")
        else:
            self.withDensityCheckbox.configure(text="禁用")
        self.withDensityCheckbox.update()


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
        self.eventBus = EventBusNamespace.register(name)
        EventBusNamespace.set(name, component=self)

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

        self.after(20, lambda: self.eventBus.broadcast("init", self))
