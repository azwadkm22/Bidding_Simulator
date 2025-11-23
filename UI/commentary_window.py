import tkinter as tk
from tkinter import ttk
from UI.ui_core import get_root

_commentary_window = None
_commentary_labels = {}

SPEAKERS = ["Troy", "Abed"]

def _create_commentary_window():
    global _commentary_window, _commentary_labels

    root = get_root()
    _commentary_window = tk.Toplevel(root)
    _commentary_window.title("commentary Info")

    screen_w = _commentary_window.winfo_screenwidth()
    x = screen_w - 450
    _commentary_window.geometry(f"400x700+{x}+250")

    frame = ttk.Frame(_commentary_window, padding=20)
    frame.pack(fill="both", expand=True)

    _commentary_labels["frame"] = frame


def _update_commentary_window(comments):
    frame = _commentary_labels["frame"]

    for c in frame.winfo_children():
        c.destroy()

    for i in range(len(comments)):
        speaker = SPEAKERS[i % 2]
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=2)
        
        # 1. Label for the Speaker (fixed width)
        ttk.Label(row, text=f"{speaker}:", width=10).pack(side="left")
        
        # 2. Label for the Comment (set text wrapping)
        comment_label = ttk.Label(row, text=comments[i], wraplength=250 , justify="left")
        comment_label.pack(side="left", fill="x", expand=True)



def show_commentary_info_in_window(comments):
    global _commentary_window

    if _commentary_window is None or not _commentary_window.winfo_exists():
        _create_commentary_window()

    _update_commentary_window(comments)
