import tkinter as tk

from frontend import ImageView
from frontend.builder import BuilderRoot
from services.render import Network, Render

if __name__ == "__main__":
    root = tk.Tk()
    BuilderRoot(root=root)
    root.mainloop()
