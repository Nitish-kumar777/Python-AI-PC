import tkinter as tk
from tkinter import scrolledtext
from config import gui_running

root = tk.Tk()
root.title("J.A.R.V.I.S AI System")
root.geometry("500x350")
root.configure(bg='#0a0a1a')

text_area = scrolledtext.ScrolledText(root, wrap=tk.WORD, width=70, height=20,
                                      bg='#0a0a1a', fg='#00ff00', font=('Courier New', 12))
text_area.pack(pady=20)
text_area.insert(tk.INSERT, "System initialized. Waiting for wake word...\n")
text_area.see(tk.END)

status_label = tk.Label(root, text="Status: Offline", fg='red', bg='#0a0a1a',
                        font=('Arial', 10, 'bold'))
status_label.pack()

def update_gui(message, is_user=False):
    if not gui_running:
        return
    try:
        tag = "user" if is_user else "jarvis"
        color = "#ff9900" if is_user else "#00ff00"
        text_area.tag_config(tag, foreground=color)
        text_area.insert(tk.INSERT, f"{'👤 You' if is_user else '🤖 J.A.R.V.I.S'}: {message}\n", tag)
        text_area.see(tk.END)
        root.update()
    except tk.TclError:
        pass
