import tkinter as tk
from typing import Tuple

from PIL import Image, ImageTk

from .builder import BuilderRoot


class MainApplication(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.pack()


class ImageView(tk.Frame):
    def __init__(self, root: tk.Frame, imageSize: Tuple[int, int]) -> None:
        super().__init__(root)
        self.pack()
        self.image = Image.new("RGBA", imageSize, (0x00, 0x00, 0x00, 0x00))
        self.imageSize = imageSize
        self.imageLabel = tk.Label(
            master=self,
            image=ImageTk.PhotoImage(
                image=self.image, size=self.imageSize
            ),  # type:ignore
        )
        self.imageLabel.grid(column=0, row=0, sticky=tk.S)

        self.pack()
        self.imageLabel.pack()

    def setImage(self, image: Image.Image):
        self.image = image.resize(self.imageSize)
        self.imageLabel.configure(
            image=ImageTk.PhotoImage(
                image=self.image, size=self.imageSize
            )  # type:ignore
        )
        self.update()


BuilderRoot["main"] = MainApplication
BuilderRoot["main"]["imageview"] = ImageView
BuilderRoot["main"]["imageview"].setInitArgs(imageSize=(200, 200))
