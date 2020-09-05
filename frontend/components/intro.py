import tkinter as tk
from tkinter.font import Font as TkFont
from typing import List


class IntroRoot(tk.Frame):
    def __init__(self, root: tk.Widget, *, content: str):
        super().__init__(root)
        self.contents: List[tk.Label] = []
        for line in content.strip().splitlines():
            label = tk.Label(
                master=self,
                text=line,
                justify=tk.LEFT,
                font=(
                    TkFont(size=20, weight="bold") if line.startswith("#") else TkFont()
                ),
            )
            self.contents.append(label)
        for row in range(len(self.contents)):
            self.contents[row].grid(column=0, row=row, sticky=tk.W)