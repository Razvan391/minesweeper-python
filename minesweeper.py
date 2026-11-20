import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root):
        self.root = root
        self.root.title("Minesweeper Python")
        self.root.resizable(False, False)
        
        # Configurații: (rânduri_verticală, coloane_laterală, număr_bombe)
        self.difficulties = {
            "Easy": (9, 9, 10),
            "Medium": (12, 12, 22),
            "Hard": (20, 9, 35)
        }
        
        self.current_diff = "Easy"
        self.top_frame = tk.Frame(self.root, pady=5)
        self.top_frame.pack()
        
        self.board_frame = tk.Frame(self.root)
        self.board_frame.pack(padx=5, pady=5)
        
        self.setup_difficulty_bar()
        self.start_game("Easy")
        
    def setup_difficulty_bar(self):
        """Creează butoanele de selectare a dificultății."""
        for diff_name in self.difficulties:
            btn = tk.Button(
                self.top_frame,
                text=diff_name,
                width=8,
                font=("Helvetica", 10, "bold"),
                command=lambda d=diff_name: self.start_game(d)
            )
            btn.pack(side=tk.LEFT, padx=3)

    def start_game(self, difficulty):
        """Resetează tabla și inițializează un joc nou pe dificultatea aleasă."""
        self.current_diff = difficulty
        self.rows, self.cols, self.mines_count = self.difficulties[difficulty]
        
        # Curăță tabla anterioară
        for widget in self.board_frame.winfo_children():
            widget.destroy()
            
        self.buttons = {}
        self.mine_positions = set()
        self.revealed_count = 0
        self.game_over = False
        
        self.setup_ui()
        self.place_mines()

    def setup_ui(self):
        """Creează grila de butoane pe ecran."""
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(
                    self.board_frame, 
                    text="", 
                    width=3, 
                    height=1, 
                    font=("Helvetica", 11, "bold"),
                    bg="#c0c0c0",
                    relief="raised"
                )
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.on_click(r, c))
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = {
                    "widget": btn,
                    "is_mine": False,
                    "state": "hidden",
                    "adjacent_mines": 0
                }

    def place_mines(self):
        """Plasează aleatoriu bombele pe tablă și calculează vecinii."""
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mine_positions = set(random.sample(all_positions, self.mines_count))
        
        for r, c in self.mine_positions:
            self.buttons[(r, c)]["is_mine"] = True
            
        for r in range(self.rows):
            for c in range(self.cols):
                if not self.buttons[(r, c)]["is_mine"]:
                    self.buttons[(r, c)]["adjacent_mines"] = self.count_adjacent_mines(r, c)

    def count_adjacent_mines(self, r, c):
        """Numără bombele din cele 8 celule vecine (inclusiv colțuri)."""
        count = 0
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                if 0 <= nr < self.rows and 0 <= nc < self.cols:
                    if self.buttons[(nr, nc)]["is_mine"]:
                        count += 1
        return count

    def on_click(self, r, c):
        """Logica când jucătorul apasă Click Stânga (săpătura)."""
        if self.game_over:
            return
            
        cell = self.buttons[(r, c)]
        if cell["state"] != "hidden":
            return
            
        if cell["is_mine"]:
            cell["widget"].config(text="💣", bg="red")
            self.end_game(won=False)
            return

        self.reveal_cell(r, c)
        
        total_safe_cells = (self.rows * self.cols) - self.mines_count
        if self.revealed_count == total_safe_cells:
            self.end_game(won=True)

    def reveal_cell(self, r, c):
        """Descoperă o celulă și extinde automat zonele libere."""
        cell = self.buttons[(r, c)]
        if cell["state"] != "hidden":
            return
            
        cell["state"] = "revealed"
        self.revealed_count += 1
        
        mines = cell["adjacent_mines"]
        btn = cell["widget"]
        colors = {1: "blue", 2: "green", 3: "red", 4: "darkblue", 5: "maroon", 6: "cyan", 7: "black", 8: "gray"}
        
        if mines > 0:
            btn.config(text=str(mines), fg=colors.get(mines, "black"), bg="#e0e0e0", relief="sunken")
        else:
            btn.config(text="", bg="#e0e0e0", relief="sunken")
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < self.rows and 0 <= nc < self.cols:
                        self.reveal_cell(nr, nc)

    def on_right_click(self, r, c):
        """Plasare sau scoatere steguleț cu Click Dreapta."""
        if self.game_over:
            return
            
        cell = self.buttons[(r, c)]
        if cell["state"] == "revealed":
            return
            
        if cell["state"] == "hidden":
            cell["state"] = "flagged"
            cell["widget"].config(text="🚩", fg="red")
        elif cell["state"] == "flagged":
            cell["state"] = "hidden"
            cell["widget"].config(text="")

    def end_game(self, won):
        """Afișează mesajul de final și dezvăluie toate bombele."""
        self.game_over = True
        
        for (r, c), cell in self.buttons.items():
            if cell["is_mine"]:
                if not won:
                    cell["widget"].config(text="💣", bg="#ff9999" if cell["widget"]["bg"] != "red" else "red")
                else:
                    cell["widget"].config(text="🚩", fg="green")
                    
        if won:
            messagebox.showinfo("Minesweeper", f"Felicitări! Ai câștigat pe nivelul {self.current_diff}!")
        else:
            messagebox.showerror("Minesweeper", "BOOM! Ai călcat pe o bombă. Apasă pe o dificultate pentru a reîncepe.")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root)
    root.mainloop()