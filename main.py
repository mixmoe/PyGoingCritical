import tkinter as tk

from frontend import MainApplication

if __name__ == "__main__":
    root = tk.Tk()
    main = MainApplication(root)
    main.pack()
    root.mainloop()
