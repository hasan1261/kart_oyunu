import tkinter as tk
from tkinter import messagebox
import random

class MemoryGame:
    def __init__(self, master):
        self.master = master
        self.master.title("Hafıza Oyunu")

        self.rows, self.cols = 4, 5
        self.score = 0
        self.matches = 0
        self.selected = []

        self.grid = self.create_grid()
        self.revealed = [[False] * self.cols for _ in range(self.rows)]
        self.buttons = [[None] * self.cols for _ in range(self.rows)]

        self.time_left = 80
        self.create_widgets()
        self.update_timer()

    def create_grid(self):
        numbers = random.sample(range(1, 51), 10) * 2
        random.shuffle(numbers)
        return [numbers[i:i + self.cols] for i in range(0, len(numbers), self.cols)]

    def create_widgets(self):
        for r in range(self.rows):
            for c in range(self.cols):
                btn = tk.Button(self.master, text="❓", width=6, height=3,
                                command=lambda r=r, c=c: self.on_click(r, c), bg="SystemButtonFace")
                btn.grid(row=r, column=c, padx=5, pady=5)
                self.buttons[r][c] = btn

        self.status = tk.Label(self.master, text=f"Puan: {self.score}", font=("Arial", 14))
        self.status.grid(row=self.rows, column=0, columnspan=self.cols//2)

        self.timer_label = tk.Label(self.master, text=f"Süre: {self.time_left}", font=("Arial", 14))
        self.timer_label.grid(row=self.rows, column=self.cols//2, columnspan=self.cols//2)

    def on_click(self, r, c):
        if self.revealed[r][c] or len(self.selected) == 2:
            return

        self.revealed[r][c] = True
        self.buttons[r][c].config(text=str(self.grid[r][c]), bg="light blue")
        self.selected.append((r, c))

        if len(self.selected) == 2:
            self.master.after(500, self.check_match)

    def check_match(self):
        r1, c1 = self.selected[0]
        r2, c2 = self.selected[1]

        if self.grid[r1][c1] == self.grid[r2][c2]:
            self.score += 10
            self.matches += 1
            self.buttons[r1][c1].config(bg="light green")
            self.buttons[r2][c2].config(bg="light green")
        else:
            self.score -= 3
            self.revealed[r1][c1] = False
            self.revealed[r2][c2] = False
            self.buttons[r1][c1].config(text=str(self.grid[r1][c1]), bg="red")
            self.buttons[r2][c2].config(text=str(self.grid[r2][c2]), bg="red")
            self.master.after(500, lambda: self.reset_buttons(r1, c1, r2, c2))

        self.selected = []
        self.status.config(text=f"Puan: {self.score}")

        if self.matches == 10:
            self.end_game()

    def reset_buttons(self, r1, c1, r2, c2):
        self.buttons[r1][c1].config(text="❓", bg="SystemButtonFace")
        self.buttons[r2][c2].config(text="❓", bg="SystemButtonFace")

    def update_timer(self):
        if self.matches == 10:
            return  
        if self.time_left > 0:
            self.time_left -= 1
            self.timer_label.config(text=f"Süre: {self.time_left}")
            self.master.after(1000, self.update_timer)
        else:
            self.end_game(timeout=True)

    def end_game(self, timeout=False):
        if timeout:
            messagebox.showinfo("Süre Doldu", f"Süre bitti! Toplam Puan: {self.score}")
        else:
            messagebox.showinfo("Oyun Bitti", f"Tebrikler! Toplam Puan: {self.score}")
        self.master.quit()

def main():
    root = tk.Tk()
    game = MemoryGame(root)
    root.mainloop()

if __name__ == "__main__":
    main()
