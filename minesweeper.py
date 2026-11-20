import tkinter as tk
from tkinter import messagebox
import random

class Minesweeper:
    def __init__(self, root, rows=9, cols=9, mines=10):
        self.root = root
        self.root.title("Minesweeper Python")
        
        self.rows = rows
        self.cols = cols
        self.mines_count = mines
        
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
                    self.root, 
                    text="", 
                    width=3, 
                    height=1, 
                    font=("Helvetica", 12, "bold"),
                    bg="#c0c0c0",
                    relief="raised"
                )
                # Click stânga pentru a săpa (descoperi)
                btn.bind("<Button-1>", lambda e, r=r, c=c: self.on_click(r, c))
                # Click dreapta pentru a pune/scoate stegulețul
                btn.bind("<Button-3>", lambda e, r=r, c=c: self.on_right_click(r, c))
                
                btn.grid(row=r, column=c)
                self.buttons[(r, c)] = {
                    "widget": btn,
                    "is_mine": False,
                    "state": "hidden",  # "hidden", "revealed", "flagged"
                    "adjacent_mines": 0
                }

    def place_mines(self):
        """Plasează aleatoriu bombele pe tablă și calculează vecinii."""
        all_positions = [(r, c) for r in range(self.rows) for c in range(self.cols)]
        self.mine_positions = set(random.sample(all_positions, self.mines_count))
        
        for r, c in self.mine_positions:
            self.buttons[(r, c)]["is_mine"] = True
            
        # Calculează numărul de bombe adiacente pentru fiecare celulă
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
        
        # Ignoră celulele deja descoperite sau marcate cu steguleț
        if cell["state"] != "hidden":
            return
            
        # AI LOVIT O BOMBĂ!
        if cell["is_mine"]:
            cell["widget"].config(text="💣", bg="red")
            self.end_game(won=False)
            return

        # Săpătură în celulă sigură
        self.reveal_cell(r, c)
        
        # Verifică dacă ai câștigat
        total_safe_cells = (self.rows * self.cols) - self.mines_count
        if self.revealed_count == total_safe_cells:
            self.end_game(won=True)

    def reveal_cell(self, r, c):
        """Descoperă o celulă și extinde automat zonele libere (Recursivitate)."""
        cell = self.buttons[(r, c)]
        if cell["state"] != "hidden":
            return
            
        cell["state"] = "revealed"
        self.revealed_count += 1
        
        mines = cell["adjacent_mines"]
        btn = cell["widget"]
        
        # Culori specifice pentru fiecare număr
        colors = {1: "blue", 2: "green", 3: "red", 4: "darkblue", 5: "maroon", 6: "cyan", 7: "black", 8: "gray"}
        
        if mines > 0:
            btn.config(text=str(mines), fg=colors.get(mines, "black"), bg="#e0e0e0", relief="sunken")
        else:
            # Dacă sunt 0 bombe vecine, lasă spațiu gol și deschide automat vecinii
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
        
        # Arată toate bombele
        for (r, c), cell in self.buttons.items():
            if cell["is_mine"]:
                if not won:
                    cell["widget"].config(text="💣", bg="#ff9999" if cell["widget"]["bg"] != "red" else "red")
                else:
                    cell["widget"].config(text="🚩", fg="green")
                    
        if won:
            messagebox.showinfo("Minesweeper", "Felicitări! Ai găsit toate zonele libere și ai evitat bombele!")
        else:
            messagebox.showerror("Minesweeper", "BOOM! Ai călcat pe o bombă. Joc încheiat!")

if __name__ == "__main__":
    root = tk.Tk()
    game = Minesweeper(root, rows=9, cols=9, mines=10)
    root.mainloop()