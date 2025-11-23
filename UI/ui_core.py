import tkinter as tk
import threading

_root = None
_root_started = False


def get_root():
    """Returns the global Tk root, creating it if needed."""
    global _root, _root_started

    if _root is None:
        _root = tk.Tk()
        _root.withdraw()

    if not _root_started:
        thread = threading.Thread(target=_root.mainloop, daemon=True)
        thread.start()
        _root_started = True

    return _root
