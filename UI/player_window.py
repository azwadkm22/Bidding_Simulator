import tkinter as tk
from tkinter import ttk
from UI.ui_core import get_root
from Manager.player_manager import get_player

_player_window = None
_player_labels = {}


def _create_player_window():
    global _player_window, _player_labels

    root = get_root()
    _player_window = tk.Toplevel(root)
    _player_window.title("Player Info")
    _player_window.geometry("350x400+50+50")

    frame = ttk.Frame(_player_window, padding=20)
    frame.pack(fill="both", expand=True)

    _player_labels["frame"] = frame


def _update_player_window(player_data):
    frame = _player_labels["frame"]

    # remove old
    for c in frame.winfo_children():
        c.destroy()

    # add new
    for k, v in player_data.items():
        row = ttk.Frame(frame)
        row.pack(fill="x", pady=2)
        ttk.Label(row, text=f"{k}:", width=18).pack(side="left")
        ttk.Label(row, text=str(v)).pack(side="left")


def show_player_info_in_window(player_id):
    global _player_window

    player_data = get_player(str(player_id))
    if not player_data:
        print("Player not found.")
        return

    if _player_window is None or not _player_window.winfo_exists():
        _create_player_window()

    _update_player_window(player_data)
