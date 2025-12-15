# Alarmo/main.py

import tkinter as tk
from gui.alarmo_app import AlarmoApp

if __name__ == "__main__":
    root = tk.Tk()
    app = AlarmoApp(root)
    root.protocol("WM_DELETE_WINDOW", app.on_closing)
    root.mainloop()