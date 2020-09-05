# flake8:noqa:F401
import tkinter as tk

from .builder import BuilderRoot
from .components.interactive import InteractiveRoot
from .components.tab import TabSwitcherRoot


class MainApplication(tk.Frame):
    def __init__(self, root: tk.Tk) -> None:
        super().__init__(root)
        self.pack()

        from . import SIRmodel


BuilderRoot["main"] = MainApplication
BuilderRoot["main"]["tab"] = TabSwitcherRoot
BuilderRoot["main"]["tab"]["SIRmodel"] = InteractiveRoot
BuilderRoot["main"]["tab"]["SISmodel"] = InteractiveRoot
BuilderRoot["main"]["tab"]["AdvancedSISmodel"] = InteractiveRoot
BuilderRoot["main"]["tab"]["SIRmodel"].setInitArgs(name="SIRmodel")
BuilderRoot["main"]["tab"]["SISmodel"].setInitArgs(name="SISmodel", enableRecovery=True)
BuilderRoot["main"]["tab"]["AdvancedSISmodel"].setInitArgs(
    name="AdvancedSISmodel", enableRecovery=True, enableDensity=True
)
