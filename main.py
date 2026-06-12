import tkinter as tk
from tkinter import messagebox
import random
import json
import os
from datetime import datetime

LEADERBOARD_FILE = "leaderboard.json"

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

def load_leaderboard():
    if os.path.exists(LEADERBOARD_FILE):
        with open(LEADERBOARD_FILE, "r") as f:
            return json.load(f)
    return []

def save_score(name, score, difficulty, size):
    data = load_leaderboard()
    data.append({
        "name": name,
        "score": score,
        "difficulty": difficulty,
        "grid_size": size,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M"),
    })
    with open(LEADERBOARD_FILE, "w") as f:
        json.dump(data, f, indent=2)

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

    btn_row2 = tk.Frame(frame, bg=BG_COLOR)
    btn_row2.pack(pady=(0, 40))

    tk.Button(btn_row2, text="▶   Play", command=on_play,
              font=("Helvetica", 14, "bold"),
              bg=ACCENT, fg="white",
              activebackground=ACCENT_DARK, activeforeground="white",
              relief="flat", padx=32, pady=12,
              cursor="hand2", bd=0).pack(side="left", padx=6)

    tk.Button(btn_row2, text="🏆   Leaderboard",
              command=lambda: switch_frame(build_leaderboard()),
              font=("Helvetica", 14, "bold"),
              bg=BUTTON_BG, fg=TEXT_LIGHT,
              activebackground=BUTTON_HOVER, activeforeground="white",
              relief="flat", padx=24, pady=12,
              cursor="hand2", bd=0).pack(side="left", padx=6)

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

    tk.Button(header, text="🏆 Board",
              command=lambda: switch_frame(build_leaderboard()),
              font=("Helvetica", 10),
              bg=BUTTON_BG, fg=TEXT_LIGHT,
              activebackground=BUTTON_HOVER,
              relief="flat", padx=12, pady=5,
              cursor="hand2", bd=0).pack(side="right", padx=4, pady=8)

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
            return  

        moved = board.move(direction)
        if not moved:
            return 

        draw_board()

        if board.is_game_over():
            save_score(player_name, board.score, difficulty, size)
            go_to_board = messagebox.askyesno(
                "Game Over",
                f"No more moves left!\n\nFinal score: {board.score}\n\nView Leaderboard?"
            )
            if go_to_board:
                switch_frame(build_leaderboard())
            else:
                switch_frame(build_menu())

    frame.bind_all("<Key>", on_key_press)

    return frame

def build_leaderboard():
    frame = tk.Frame(root, bg=BG_COLOR)

    header = tk.Frame(frame, bg=CARD_COLOR)
    header.pack(fill="x")

    tk.Label(header, text="🏆  Leaderboard",
             font=("Helvetica", 22, "bold"),
             fg=ACCENT, bg=CARD_COLOR).pack(side="left", padx=16, pady=12)

    tk.Button(header, text="↩ Menu", command=lambda: switch_frame(build_menu()),
              font=("Helvetica", 11),
              bg=BUTTON_BG, fg=TEXT_LIGHT,
              activebackground=BUTTON_HOVER,
              relief="flat", padx=12, pady=6,
              cursor="hand2", bd=0).pack(side="right", padx=12, pady=8)

    filter_bar = tk.Frame(frame, bg=BG_COLOR)
    filter_bar.pack(fill="x", padx=16, pady=10)

    tk.Label(filter_bar, text="Filter:",
             font=("Helvetica", 10), fg="#aaaaaa", bg=BG_COLOR).pack(side="left")

    filter_var = tk.StringVar(value="All")

    def update_filter_buttons():
        for widget in filter_bar.winfo_children():
            if isinstance(widget, tk.Radiobutton):
                if widget.cget("text") == filter_var.get():
                    widget.config(bg=ACCENT, fg="white")
                else:
                    widget.config(bg=BUTTON_BG, fg=TEXT_LIGHT)

    for option in ("All", "Easy", "Medium", "Hard"):
        rb = tk.Radiobutton(filter_bar, text=option, variable=filter_var,
                            value=option,
                            command=lambda: (update_filter_buttons(), refresh_list()),
                            font=("Helvetica", 10),
                            fg=TEXT_LIGHT, bg=BUTTON_BG,
                            activebackground=BUTTON_HOVER,
                            activeforeground="white",
                            selectcolor=ACCENT, indicatoron=0,
                            relief="flat", padx=10, pady=4, cursor="hand2")
        rb.pack(side="left", padx=4)

    tk.Label(filter_bar, text="   Search:",
             font=("Helvetica", 10), fg="#aaaaaa", bg=BG_COLOR).pack(side="left", padx=(10, 4))

    search_var = tk.StringVar()
    search_entry = tk.Entry(filter_bar, textvariable=search_var,
                            font=("Helvetica", 11),
                            bg="#2a2a4a", fg=TEXT_LIGHT,
                            insertbackground=TEXT_LIGHT,
                            relief="flat", bd=6, width=14)
    search_entry.pack(side="left")

    list_frame = tk.Frame(frame, bg=BG_COLOR)
    list_frame.pack(fill="both", expand=True, padx=16, pady=(0, 16))

    col_header = tk.Frame(list_frame, bg=CARD_COLOR)
    col_header.pack(fill="x")
    for label, width in [("#", 4), ("Player", 16), ("Score", 10),
                          ("Difficulty", 10), ("Grid", 8), ("Date", 16)]:
        tk.Label(col_header, text=label, font=("Helvetica", 10, "bold"),
                 fg=ACCENT, bg=CARD_COLOR, width=width, anchor="w").pack(
            side="left", padx=6, pady=6)

    rows_frame = tk.Frame(list_frame, bg=BG_COLOR)
    rows_frame.pack(fill="both", expand=True)

    def refresh_list():
        for widget in rows_frame.winfo_children():
            widget.destroy()

        data = load_leaderboard()

        chosen_filter = filter_var.get()
        if chosen_filter != "All":
            data = [entry for entry in data if entry.get("difficulty") == chosen_filter]

        search_text = search_var.get().strip().lower()
        if search_text:
            data = [entry for entry in data if search_text in entry.get("name", "").lower()]

        data.sort(key=lambda entry: entry.get("score", 0), reverse=True)

        if not data:
            tk.Label(rows_frame, text="No entries yet — play a game first!",
                     font=("Helvetica", 12), fg="#666688", bg=BG_COLOR).pack(pady=40)
            return

        for i, entry in enumerate(data):
            row_bg = "#1f1f3a" if i % 2 == 0 else BG_COLOR
            row = tk.Frame(rows_frame, bg=row_bg)
            row.pack(fill="x")

            rank_text = str(i + 1)
            if i == 0:
                rank_text = "🥇"
            elif i == 1:
                rank_text = "🥈"
            elif i == 2:
                rank_text = "🥉"

            values = [
                (rank_text, 4),
                (entry.get("name", "-"), 16),
                (str(entry.get("score", 0)), 10),
                (entry.get("difficulty", "-"), 10),
                (f"{entry.get('grid_size', '?')}×{entry.get('grid_size', '?')}", 8),
                (entry.get("date", "-"), 16),
            ]
            for text, width in values:
                tk.Label(row, text=text, font=("Helvetica", 11),
                         fg=TEXT_LIGHT, bg=row_bg, width=width, anchor="w").pack(
                    side="left", padx=6, pady=5)

    search_var.trace_add("write", lambda *args: refresh_list())
    update_filter_buttons()
    refresh_list()

    return frame

switch_frame(build_menu())

root.update_idletasks()
w, h = root.winfo_width(), root.winfo_height()
sw, sh = root.winfo_screenwidth(), root.winfo_screenheight()
root.geometry(f"+{(sw - w) // 2}+{(sh - h) // 2}")

root.mainloop()