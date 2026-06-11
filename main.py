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

card = tk.Frame(root, bg=CARD_COLOR)
card.pack(padx=60, pady=4, fill="x")   # fill="x" stretches it horizontally
 
# ── Player name ───────────────────────────────────────────────────────────────
tk.Label(card, text="Player Name",
         font=("Helvetica", 11, "bold"),
         fg=TEXT_LIGHT, bg=CARD_COLOR).pack(padx=20, pady=(16, 4), anchor="w")

name_var = tk.StringVar()

name_entry = tk.Entry(card,
                      textvariable=name_var,       # links entry to name_var
                      font=("Helvetica", 13),
                      bg="#2a2a4a", fg=TEXT_LIGHT,
                      insertbackground=TEXT_LIGHT, # cursor color
                      relief="flat", bd=8)
name_entry.pack(padx=20, pady=(0, 14), fill="x")
name_entry.focus()   # put keyboard focus here on launch