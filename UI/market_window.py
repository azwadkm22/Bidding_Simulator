import tkinter as tk
from tkinter import ttk
from UI.ui_core import get_root

_market_window = None
_market_labels = {}


def _create_market_window():
    global _market_window, _market_labels

    root = get_root()
    _market_window = tk.Toplevel(root)
    _market_window.title("Market Status")

    screen_w = _market_window.winfo_screenwidth()
    x = screen_w - 350
    _market_window.geometry(f"300x150+{x}+50")

    frame = ttk.Frame(_market_window, padding=20)
    frame.pack(fill="both", expand=True)

    _market_labels["sold"] = ttk.Label(frame, text="Sold: 0")
    _market_labels["sold"].pack(anchor="w", pady=5)

    _market_labels["remaining"] = ttk.Label(frame, text="Remaining: 0")
    _market_labels["remaining"].pack(anchor="w", pady=5)

    _market_labels["unsold"] = ttk.Label(frame, text="Unsold: 0")
    _market_labels["unsold"].pack(anchor="w", pady=5)


def show_market_status_window(sold, remaining, unsold):
    global _market_window

    if _market_window is None or not _market_window.winfo_exists():
        _create_market_window()

    _market_labels["sold"].config(text=f"Sold: {sold}")
    _market_labels["remaining"].config(text=f"Remaining: {remaining}")
    _market_labels["unsold"].config(text=f"Unsold: {unsold}")
