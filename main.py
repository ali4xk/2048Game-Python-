import tkinter as tk
from tkinter import messagebox
import random

BG_COLOR     = "#1a1a2e"
CARD_COLOR   = "#16213e"
BOARD_BG     = "#0f3460"
GRID_COLOR   = "#533483"
ACCENT       = "#e94560"
ACCENT_DARK  = "#c73652"
BUTTON_BG    = "#533483"
BUTTON_HOVER = "#6a45a8"
TEXT_LIGHT   = "#e0e0e0"

TILE_COLORS = {
    0:    ("#cdc1b4", "#776e65"),
    2:    ("#eee4da", "#776e65"),
    4:    ("#ede0c8", "#776e65"),
    8:    ("#f2b179", "#f9f6f2"),
    16:   ("#f59563", "#f9f6f2"),
    32:   ("#f67c5f", "#f9f6f2"),
    64:   ("#f65e3b", "#f9f6f2"),
    128:  ("#edcf72", "#f9f6f2"),
    256:  ("#edcc61", "#f9f6f2"),
    512:  ("#edc850", "#f9f6f2"),
    1024: ("#edc53f", "#f9f6f2"),
    2048: ("#edc22e", "#f9f6f2"),
}

DIFFICULTY = {
    "Easy":   4,
    "Medium": 6,
    "Hard":   10,
}

class Board:
    def __init__(self, size):
        self.size = size
        self.score = 0
        self.grid = [[0] * size for _ in range(size)]
        self.spawn_tile()
        self.spawn_tile()

    def spawn_tile(self):
        empty_cells = []
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    empty_cells.append((r, c))
        if not empty_cells:
            return
        r, c = random.choice(empty_cells)
        self.grid[r][c] = 4 if random.random() < 0.1 else 2

    def _compress_row(self, row):
        non_zero = [value for value in row if value != 0]
        non_zero += [0] * (self.size - len(non_zero))
        return non_zero

    def _merge_row(self, row):
        for i in range(self.size - 1):
            if row[i] != 0 and row[i] == row[i + 1]:
                row[i] = row[i] * 2
                self.score += row[i]
                row[i + 1] = 0
        return row

    def _slide_row_left(self, row):
        row = self._compress_row(row)
        row = self._merge_row(row)
        row = self._compress_row(row)
        return row

    def _rotate_cw(self):
        self.grid = [list(row) for row in zip(*self.grid[::-1])]

    def _rotate_ccw(self):
        self.grid = [list(row) for row in zip(*self.grid)][::-1]

    def move(self, direction):

        before = [row[:] for row in self.grid]   # row[:] makes a copy of each row

        if direction == "left":
            self.grid = [self._slide_row_left(row) for row in self.grid]

        elif direction == "right":
            self.grid = [row[::-1] for row in self.grid]
            self.grid = [self._slide_row_left(row) for row in self.grid]
            self.grid = [row[::-1] for row in self.grid]

        elif direction == "up":
            self._rotate_ccw()
            self.grid = [self._slide_row_left(row) for row in self.grid]
            self._rotate_cw()

        elif direction == "down":
            self._rotate_cw()
            self.grid = [self._slide_row_left(row) for row in self.grid]
            self._rotate_ccw()

        changed = (self.grid != before)
        if changed:
            self.spawn_tile()
        return changed

    def is_game_over(self):
        for r in range(self.size):
            for c in range(self.size):
                if self.grid[r][c] == 0:
                    return False
                if c + 1 < self.size and self.grid[r][c] == self.grid[r][c + 1]:
                    return False
                if r + 1 < self.size and self.grid[r][c] == self.grid[r + 1][c]:
                    return False
        return True

root = tk.Tk()
root.title("2048")
root.configure(bg=BG_COLOR)
root.resizable(False, False)

current_frame = None

def switch_frame(new_frame):
    global current_frame
    if current_frame is not None:
        current_frame.destroy()
    current_frame = new_frame
    current_frame.pack(fill="both", expand=True)

def build_menu():
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
        "Easy: 4×4   |   Medium: 6×6   |   Hard: 10×10\n"
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
        switch_frame(build_game(name, chosen_diff, chosen_size))

    tk.Button(frame, text="▶   Play", command=on_play,
              font=("Helvetica", 14, "bold"),
              bg=ACCENT, fg="white",
              activebackground=ACCENT_DARK, activeforeground="white",
              relief="flat", padx=32, pady=12,
              cursor="hand2", bd=0).pack(pady=(0, 40))

    return frame

def build_game(player_name, difficulty, size):
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

    score_label = tk.Label(header, text="Score: 0",
                           font=("Helvetica", 13, "bold"),
                           fg=TEXT_LIGHT, bg=CARD_COLOR)
    score_label.pack(side="right", padx=16)

    def back_to_menu():
        switch_frame(build_menu())

    tk.Button(header, text="↩ Menu", command=back_to_menu,
              font=("Helvetica", 10),
              bg=BUTTON_BG, fg=TEXT_LIGHT,
              activebackground=BUTTON_HOVER,
              relief="flat", padx=12, pady=5,
              cursor="hand2", bd=0).pack(side="right", padx=12, pady=8)

    PADDING = 6
    if size <= 4:
        cell_px = 80
    elif size <= 6:
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
        x0 = PADDING + c * (cell_px + PADDING)
        y0 = PADDING + r * (cell_px + PADDING)
        return x0, y0, x0 + cell_px, y0 + cell_px

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
        for r in range(size):
            for c in range(size):
                value = board.grid[r][c]
                bg, fg = TILE_COLORS.get(value, ("#3c3a32", "#f9f6f2"))
                lbl = tile_labels[(r, c)]
                lbl.config(text=str(value) if value else "", bg=bg, fg=fg)
        score_label.config(text=f"Score: {board.score}")

    draw_board()

    KEY_MAP = {
        "Left":  "left",  "a": "left",  "A": "left",
        "Right": "right", "d": "right", "D": "right",
        "Up":    "up",    "w": "up",    "W": "up",
        "Down":  "down",  "s": "down",  "S": "down",
    }

    def on_key_press(event):
        direction = KEY_MAP.get(event.keysym)
        if direction is None:
            return  # ignore any key we don't care about

        moved = board.move(direction)
        if not moved:
            return  # nothing changed (e.g. pressed left but already at left wall)

        draw_board()

        if board.is_game_over():
            messagebox.showinfo("Game Over",
                                f"No more moves left!\n\nFinal score: {board.score}")
            switch_frame(build_menu())

    frame.bind_all("<Key>", on_key_press)

    return frame

switch_frame(build_menu())

root.update_idletasks()
w, h = root.winfo_width(), root.winfo_height()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

root.mainloop()