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

tk.Label(card, text="Difficulty",
         font=("Helvetica", 11, "bold"),
         fg=TEXT_LIGHT, bg=CARD_COLOR).pack(padx=20, pady=(0, 6), anchor="w")
 
diff_var = tk.StringVar(value="Medium")  # default selection
 
btn_row = tk.Frame(card, bg=CARD_COLOR)
btn_row.pack(padx=20, pady=(0, 20), fill="x")
 
def update_diff_buttons():
    """Re-color radio buttons so the selected one looks highlighted."""
    for widget in btn_row.winfo_children():
        if isinstance(widget, tk.Radiobutton):
            if widget.cget("text") == diff_var.get():
                widget.config(bg=ACCENT, fg="white")
            else:
                widget.config(bg=BUTTON_BG, fg=TEXT_LIGHT)

for difficulty in ("Easy", "Medium", "Hard"):
    rb = tk.Radiobutton(btn_row,
                        text=difficulty,
                        variable=diff_var,    # all three share the same variable
                        value=difficulty,     # what diff_var becomes when clicked
                        command=update_diff_buttons,
                        font=("Helvetica", 12),
                        fg=TEXT_LIGHT, bg=BUTTON_BG,
                        activebackground=BUTTON_HOVER,
                        activeforeground="white",
                        selectcolor=ACCENT,
                        indicatoron=0,        # makes it look like a button
                        relief="flat",
                        padx=18, pady=7,
                        cursor="hand2")
    rb.pack(side="left", padx=(0, 8))
 
update_diff_buttons()  # apply colors for the default selection

rules = (
    "Easy: 6×6   |   Medium: 10×10   |   Hard: 15×15\n"
    "Use arrow keys ← ↑ → ↓ to slide tiles.\n"
    "Merge matching tiles to score. Fill the board = game over!"
)
tk.Label(root, text=rules,
         font=("Helvetica", 10),
         fg="#666688", bg=BG_COLOR,
         justify="center").pack(pady=(8, 20))

def on_play():
    """Validate inputs and (for now) just print what was chosen."""
    name = name_var.get().strip()
 
    if not name:
        # messagebox.showwarning pops up a small warning dialog
        messagebox.showwarning("Name Required", "Please enter your player name.")
        return
 
    if " " in name:
        messagebox.showwarning("No Spaces", "Player name cannot contain spaces.")
        return
 
    chosen_diff = diff_var.get()
    chosen_size = DIFFICULTY[chosen_diff]
 
    messagebox.showinfo(
        "Starting game…",
        f"Player : {name}\n"
        f"Mode   : {chosen_diff} ({chosen_size}×{chosen_size} grid)\n\n"
        "(Game board coming in Step 2!)"
    )