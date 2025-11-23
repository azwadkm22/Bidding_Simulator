# team_window.py
import json
import tkinter as tk
from tkinter import ttk
from UI.ui_core import get_root
from Manager.player_manager import get_many

_team_window = None
_team_tabs = {}

def _populate_team_tab_with_tree(frame, team_name, players, bought_for):
    # Title
    title_label = ttk.Label(frame, text=f"{team_name} Squad",
                            font=("Arial", 18, "bold"))
    title_label.pack(anchor="w", pady=(0, 8))

    container = ttk.Frame(frame)
    container.pack(fill="both", expand=True)

    columns = ("name", "position", "batting", "bowling", "bought_at")
    tree = ttk.Treeview(container, columns=columns, show="headings", selectmode="browse")
    tree.pack(side="left", fill="both", expand=True)

    col_settings = {
        "name":      ("Name", 300, "w"),
        "position":  ("Position", 150, "w"),
        "batting":   ("Batting", 90, "center"),
        "bowling":   ("Bowling", 90, "center"),
        "bought_at": ("Bought At", 100, "center"),
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
            bought_for[i],
        ))

    frame._team_tree = tree


def _create_team_window(team_dict):
    global _team_window, _team_tabs

    root = get_root()
    
    _team_window = tk.Toplevel(root)
    _team_window.title("Team Squad Information")
    _team_window.geometry("900x600+100+150")

    notebook = ttk.Notebook(_team_window, name="notebook")
    notebook.pack(fill="both", expand=True)

    _team_tabs.clear()

    for team_name, player_ids in team_dict.items():
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=team_name)

        _team_tabs[team_name] = frame
        _populate_team_tab_with_tree(frame, team_name, [], [])


def _update_tabs(team_dict, player_sold_dict):
    global _team_window, _team_tabs

    notebook = _team_window.children.get("notebook")
    if not notebook:
        return

    # Remove old tabs
    for tab_id in notebook.tabs():
        notebook.forget(tab_id)

    _team_tabs.clear()

    # Create new tabs
    for team_name, player_ids in team_dict.items():
        frame = ttk.Frame(notebook, padding=10)
        notebook.add(frame, text=team_name)
        player_list = get_many(player_ids)
        bought_for = []
        for p_id in player_ids:
            bought_for.append(player_sold_dict[p_id])

        _team_tabs[team_name] = frame
        _populate_team_tab_with_tree(frame, team_name, player_list, bought_for)


def show_team_info_window(team_dict, player_sold_dict):
    """
    team_dict format:
    {
        "Team1 Name": [101, 102],
        "Team2 Name": [103, 104, 105]
    }
    """

    global _team_window

    if not isinstance(team_dict, dict):
        print("[ERROR] Team data must be a dictionary.")
        return

    if _team_window is None or not _team_window.winfo_exists():
        _create_team_window(team_dict)
    else:
        _update_tabs(team_dict, player_sold_dict)
