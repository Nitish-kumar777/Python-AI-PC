from gui import root, update_gui
from listener import jarvis_mode
import threading

if __name__ == "__main__":
    update_gui("""
    ╔════════════════════════════╗
    ║       J.A.R.V.I.S AI       ║
    ╚════════════════════════════╝
    """)
    threading.Thread(target=jarvis_mode, daemon=True).start()
    root.mainloop()
