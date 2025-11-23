# highlight_window.py
import json
import tkinter as tk
from tkinter import ttk
from UI.ui_core import get_root
from Manager.player_manager import get_many

_highlight_window = None
_highlight_tabs = {}

def _populate_highlight_tab_with_tree(frame, highlight_name, players):
    # Title
    title_label = ttk.Label(frame, text=f"{highlight_name} Squad",
                            font=("Arial", 18, "bold"))
    title_label.pack(anchor="w", pady=(0, 8))

    container = ttk.Frame(frame)
    container.pack(fill="both", expand=True)

    columns = ("name", "position", "batting", "bowling", "estimated_price")
    tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
    tree.pack(side="left", fill="both", expand=True)

    col_settings = {
        "name":      ("Name", 180, "w"),
        "position":  ("Position", 80, "w"),
        "batting":   ("Batting", 50, "center"),
        "bowling":   ("Bowling", 50, "center"),
        "estimated_price": ("Estimated Price", 100, "center"),
    }

    for col, (text, width, anchor) in col_settings.items():
        tree.heading(col, text=text, anchor=anchor)
        tree.column(col, width=width, anchor=anchor)

    # Scrollbar
    vsb = ttk.Scrollbar(container, orient="vertical", command=tree.yview)
    vsb.pack(side="right", fill="y")
    tree.configure(yscrollcommand=vsb.set)

    # Separator
    ttk.Separator(frame, orient="horizontal").pack(fill="x", pady=8)

    # Insert row data
    for i in range(len(players)):
        tree.insert("", "end", values=(
            players[i].get("name", ""),
            players[i].get("position", ""),
            players[i].get("batting", ""),
            players[i].get("bowling", ""),
            f"{players[i].get('estimated_price', '')} Million",
        ))

    frame._highlight_tree = tree


def _create_highlight_window(highlight_dict):
    global _highlight_window, _highlight_tabs

    root = get_root()
    
    _highlight_window = tk.Toplevel(root)
    _highlight_window.title("Highlights")
    _highlight_window.geometry("600x500+450+50")

    notebook = ttk.Notebook(_highlight_window, name="notebook")
    notebook.pack(fill="both", expand=True)

    _highlight_tabs.clear()

    # Create new tabs
    for highlight_name, player_ids in highlight_dict.items():
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=highlight_name)
        player_list = get_many(player_ids)
        _highlight_tabs[highlight_name] = frame
        _populate_highlight_tab_with_tree(frame, highlight_name, player_list)


def _update_tabs(highlight_dict, player_sold_dict):
    global _highlight_window, _highlight_tabs

    notebook = _highlight_window.children.get("notebook")
    if not notebook:
        return

    # Remove old tabs
    for tab_id in notebook.tabs():
        notebook.forget(tab_id)

    _highlight_tabs.clear()

    # Create new tabs
    for highlight_name, player_ids in highlight_dict.items():
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=highlight_name)
        player_list = get_many(player_ids)
        bought_for = []
        for p_id in player_ids:
            bought_for.append(player_sold_dict[p_id])

        _highlight_tabs[highlight_name] = frame
        _populate_highlight_tab_with_tree(frame, highlight_name, player_list, bought_for)


def show_highlight_info_window(highlight_dict):
    """
    highlight_dict format:
    {
        "highlight1 Name": [101, 102],
        "highlight2 Name": [103, 104, 105]
    }
    """

    global _highlight_window

    if not isinstance(highlight_dict, dict):
        print("[ERROR] highlight data must be a dictionary.")
        return

    if _highlight_window is None or not _highlight_window.winfo_exists():
        _create_highlight_window(highlight_dict)
