import tkinter as tk
from tkinter import messagebox

BG_COLOR     = "#1a1a2e"   # dark navy  – main window background
CARD_COLOR   = "#16213e"   # slightly lighter navy – card/panel background
ACCENT       = "#e94560"   # vivid red-pink – titles, primary buttons
ACCENT_DARK  = "#c73652"   # darker shade for button hover
BUTTON_BG    = "#533483"   # purple – secondary buttons
BUTTON_HOVER = "#6a45a8"
TEXT_LIGHT   = "#e0e0e0"   # off-white – regular text

DIFFICULTY = {
    "Easy":   6,
    "Medium": 10,
    "Hard":   15,
}

root = tk.Tk()
root.title("2048")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

tk.Label(root, text="2048",
         font=("Helvetica", 72, "bold"),
         fg=ACCENT, bg=BG_COLOR).pack(pady=(40, 0))
 
tk.Label(root, text="Slide  •  Merge  •  Conquer",
         font=("Helvetica", 13),
         fg="#888888", bg=BG_COLOR).pack(pady=(0, 28))