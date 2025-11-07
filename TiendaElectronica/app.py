import tkinter as tk
from Controllers.main_controller import MainController

if __name__ == "__main__":
    root = tk.Tk()
    app = MainController(root)
    root.mainloop()