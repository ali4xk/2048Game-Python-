import tkinter as tk
from tkinter import messagebox
import random

# ─── Color palette ────────────────────────────────────────────────────────────
BG_COLOR     = "#1a1a2e"
CARD_COLOR   = "#16213e"
BOARD_BG     = "#0f3460"
GRID_COLOR   = "#533483"
ACCENT       = "#e94560"
ACCENT_DARK  = "#c73652"
BUTTON_BG    = "#533483"
BUTTON_HOVER = "#6a45a8"
TEXT_LIGHT   = "#e0e0e0"

# Color for each tile value: (background, text color)
# We'll only need a few for now since new tiles start as 2 or 4
TILE_COLORS = {
    0:  ("#cdc1b4", "#776e65"),
    2:  ("#eee4da", "#776e65"),
    4:  ("#ede0c8", "#776e65"),
    8:  ("#f2b179", "#f9f6f2"),
    16: ("#f59563", "#f9f6f2"),
}

DIFFICULTY = {
    "Easy":   6,
    "Medium": 10,
    "Hard":   15,
}

# ─── Board class ──────────────────────────────────────────────────────────────
# This class represents the game's data — the grid of numbers — completely
# separate from how it's drawn. Keeping "data" and "drawing" separate makes
# the code much easier to extend later (movement, scoring, etc.)
class Board:
    def __init__(self, size):
        self.size = size
        self.score = 0
        # Build a size×size grid filled with zeros.
        # This is a "list of lists" — grid[row][col]
        self.grid = [[0] * size for _ in range(size)]
        # Place the first two starting tiles
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        """Find all empty cells and put a 2 (90%) or 4 (10%) in a random one."""
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    empty_cells.append((r, c))

        if not empty_cells:
            return  # board is full, nothing to spawn

        r, c = random.choice(empty_cells)
        self.grid[r][c] = 4 if random.random() < 0.1 else 2


# ─── Root window ──────────────────────────────────────────────────────────────
root = tk.Tk()
root.title("2048")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

current_frame = None


def switch_frame(new_frame):
    """Destroy whatever frame is currently showing and display a new one."""
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame
    current_frame.pack(fill="both", expand=True)


# ─── MENU SCREEN ──────────────────────────────────────────────────────────────
def build_menu():
    """Create and return the menu frame (same as Step 1, slightly trimmed)."""
    frame = tk.Frame(root, bg=BG_COLOR)

    tk.Label(frame, text="2048",
             font=("Helvetica", 72, "bold"),
             fg=ACCENT, bg=BG_COLOR).pack(pady=(40, 0))

    tk.Label(frame, text="Slide  •  Merge  •  Conquer",
             font=("Helvetica", 13),
             fg="#888888", bg=BG_COLOR).pack(pady=(0, 28))

    card = tk.Frame(frame, bg=CARD_COLOR)
    card.pack(padx=60, pady=4, fill="x")

    tk.Label(card, text="Player Name",
             font=("Helvetica", 11, "bold"),
             fg=TEXT_LIGHT, bg=CARD_COLOR).pack(padx=20, pady=(16, 4), anchor="w")

    name_var = tk.StringVar()
    name_entry = tk.Entry(card, textvariable=name_var,
                          font=("Helvetica", 13),
                          bg="#2a2a4a", fg=TEXT_LIGHT,
                          insertbackground=TEXT_LIGHT,
                          relief="flat", bd=8)
    name_entry.pack(padx=20, pady=(0, 14), fill="x")
    name_entry.focus()

    tk.Label(card, text="Difficulty",
             font=("Helvetica", 11, "bold"),
             fg=TEXT_LIGHT, bg=CARD_COLOR).pack(padx=20, pady=(0, 6), anchor="w")

    diff_var = tk.StringVar(value="Medium")
    btn_row = tk.Frame(card, bg=CARD_COLOR)
    btn_row.pack(padx=20, pady=(0, 20), fill="x")

    def update_diff_buttons():
        for widget in btn_row.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                if widget.cget("text") == diff_var.get():
                    widget.config(bg=ACCENT, fg="white")
                else:
                    widget.config(bg=BUTTON_BG, fg=TEXT_LIGHT)

    for difficulty in ("Easy", "Medium", "Hard"):
        rb = tk.Radiobutton(btn_row, text=difficulty, variable=diff_var,
                            value=difficulty, command=update_diff_buttons,
                            font=("Helvetica", 12),
                            fg=TEXT_LIGHT, bg=BUTTON_BG,
                            activebackground=BUTTON_HOVER,
                            activeforeground="white",
                            selectcolor=ACCENT, indicatoron=0,
                            relief="flat", padx=18, pady=7, cursor="hand2")
        rb.pack(side="left", padx=(0, 8))

    update_diff_buttons()

    rules = (
        "Easy: 6×6   |   Medium: 10×10   |   Hard: 15×15\n"
        "Use arrow keys ← ↑ → ↓ to slide tiles.\n"
        "Merge matching tiles to score. Fill the board = game over!"
    )
    tk.Label(frame, text=rules,
             font=("Helvetica", 10),
             fg="#666688", bg=BG_COLOR,
             justify="center").pack(pady=(8, 20))

    def on_play():
        name = name_var.get().strip()
        if not name:
            messagebox.showwarning("Name Required", "Please enter your player name.")
            return
        if " " in name:
            messagebox.showwarning("No Spaces", "Player name cannot contain spaces.")
            return

        chosen_diff = diff_var.get()
        chosen_size = DIFFICULTY[chosen_diff]
        # Switch to the game screen, passing along the player's choices
        switch_frame(build_game(name, chosen_diff, chosen_size))

    tk.Button(frame, text="▶   Play", command=on_play,
              font=("Helvetica", 14, "bold"),
              bg=ACCENT, fg="white",
              activebackground=ACCENT_DARK, activeforeground="white",
              relief="flat", padx=32, pady=12,
              cursor="hand2", bd=0).pack(pady=(0, 40))

    return frame


# ─── GAME SCREEN ──────────────────────────────────────────────────────────────
def build_game(player_name, difficulty, size):
    """Create and return the game frame: a header bar + a drawn grid of tiles."""

    frame = tk.Frame(root, bg=BG_COLOR)

    board = Board(size)

    header = tk.Frame(frame, bg=CARD_COLOR)
    header.pack(fill="x")

    tk.Label(header, text="2048",
             font=("Helvetica", 24, "bold"),
             fg=ACCENT, bg=CARD_COLOR).pack(side="left", padx=16, pady=10)

    tk.Label(header, text=f"👤 {player_name}   |   {difficulty} ({size}×{size})",
             font=("Helvetica", 11),
             fg="#aaaaaa", bg=CARD_COLOR).pack(side="left", padx=10)

    def back_to_menu():
        switch_frame(build_menu())

    tk.Button(header, text="↩ Menu", command=back_to_menu,
              font=("Helvetica", 10),
              bg=BUTTON_BG, fg=TEXT_LIGHT,
              activebackground=BUTTON_HOVER,
              relief="flat", padx=12, pady=5,
              cursor="hand2", bd=0).pack(side="right", padx=12, pady=8)

    PADDING = 6
    if size <= 6:
        cell_px = 80
    elif size <= 10:
        cell_px = 50
    else:
        cell_px = 32

    board_px = cell_px * size + PADDING * (size + 1)

    canvas_frame = tk.Frame(frame, bg=BG_COLOR)
    canvas_frame.pack(padx=16, pady=16)

    canvas = tk.Canvas(canvas_frame, width=board_px, height=board_px,
                       bg=BOARD_BG, bd=0, highlightthickness=0)
    canvas.pack()

    def cell_rect(r, c):
        """Return the pixel coordinates (x0, y0, x1, y1) for grid cell (r, c)."""
        x0 = PADDING + c * (cell_px + PADDING)
        y0 = PADDING + r * (cell_px + PADDING)
        return x0, y0, x0 + cell_px, y0 + cell_px

    # Drawing the empty grid background cells once
    for r in range(size):
        for c in range(size):
            x0, y0, x1, y1 = cell_rect(r, c)
            canvas.create_rectangle(x0, y0, x1, y1, fill=GRID_COLOR, outline="")

    tile_labels = {}
    for r in range(size):
        for c in range(size):
            x0, y0, x1, y1 = cell_rect(r, c)
            cx, cy = (x0 + x1) // 2, (y0 + y1) // 2

            lbl = tk.Label(canvas, text="", bg=GRID_COLOR, fg=TEXT_LIGHT,
                          font=("Helvetica", 16, "bold"))
            canvas.create_window(cx, cy, window=lbl,
                                 width=cell_px - PADDING, height=cell_px - PADDING)
            tile_labels[(r, c)] = lbl

    def draw_board():
        """Read board.grid and update every tile Label's text and color."""
        for r in range(size):
            for c in range(size):
                value = board.grid[r][c]
                bg, fg = TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                lbl = tile_labels[(r, c)]
                lbl.config(text=str(value) if value else "", bg=bg, fg=fg)

    draw_board()

    return frame


switch_frame(build_menu())

root.update_idletasks()
w, h = root.winfo_width(), root.winfo_height()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

root.mainloop()