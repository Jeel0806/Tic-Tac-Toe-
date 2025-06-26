import tkinter as tk
from tkinter import messagebox

class TicTacToe:
    def __init__(self, root):
        self.root = root
        self.root.title("Tic Tac Toe")
        self.root.state('zoomed')
        self.size = 3  # Default board size
        self.turn = "X"
        self.winner_declared = False
        self.winner = None
        self.moves_count = 0
        self.home_page()

    def home_page(self):
        self.clear_frame()
        title_label = tk.Label(self.root, text="Welcome to Tic Tac Toe", 
                              font=("Helvetica", 24, "bold"), bg="lightblue", fg="darkblue")
        title_label.pack(pady=30)

        title_label_2 = tk.Label(self.root, text="Created by Jeel Vithalapara", 
                              font=("Helvetica", 24, "bold"), bg="lightblue", fg="darkblue")
        title_label_2.pack(pady=30)
        # Size selection UI
        size_frame = tk.Frame(self.root, bg="lightblue")
        size_frame.pack(pady=20)
        
        tk.Label(size_frame, text="Board Size (3-8):", 
                font=("Helvetica", 14), bg="lightblue").pack(side=tk.LEFT, padx=5)
                
        self.size_var = tk.StringVar(value="3")
        size_entry = tk.Entry(size_frame, textvariable=self.size_var, 
                             font=("Helvetica", 14), width=5)
        size_entry.pack(side=tk.LEFT, padx=5)
        
        play_button = tk.Button(self.root, text="Play Game", font=("Helvetica", 16), 
                               bg="green", fg="white", padx=20, pady=10, command=self.start_game)
        play_button.pack(pady=20)
        
        if self.winner:
            winner_label = tk.Label(self.root, text=f"{self.winner} Wins!", 
                                   font=("Helvetica", 18, "bold"), bg="yellow", fg="black")
            winner_label.pack(pady=20)
        elif self.winner_declared and self.moves_count == self.size**2:
            draw_label = tk.Label(self.root, text="It's a Draw!", 
                                 font=("Helvetica", 18, "bold"), bg="orange", fg="black")
            draw_label.pack(pady=20)

    def start_game(self):
        try:
            new_size = int(self.size_var.get())
            if 3 <= new_size <= 8:
                self.size = new_size
            else:
                messagebox.showwarning("Invalid Size", "Size must be between 3-8. Using default 3.")
                self.size = 3
        except ValueError:
            messagebox.showwarning("Invalid Input", "Please enter a number. Using default size 3.")
            self.size = 3
            
        self.clear_frame()
        self.create_board()

    def clear_frame(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_board(self):
        self.turn = "X"
        self.board = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.buttons = [[None for _ in range(self.size)] for _ in range(self.size)]
        self.winner_declared = False
        self.winner = None
        self.moves_count = 0

        # Configure grid for resizing
        for i in range(self.size):
            self.root.grid_rowconfigure(i, weight=1)
            self.root.grid_columnconfigure(i, weight=1)

        # Create buttons with dynamic font size
        font_size = max(8, 20 - self.size)  # Scale font based on board size
        for row in range(self.size):
            for col in range(self.size):
                btn = tk.Button(self.root, text="", font=("Helvetica", font_size),
                               command=lambda r=row, c=col: self.on_button_click(r, c))
                btn.grid(row=row, column=col, sticky="nsew", padx=2, pady=2)
                self.buttons[row][col] = btn

    def on_button_click(self, row, col):
        if self.buttons[row][col]['text'] == "" and not self.winner_declared:
            self.buttons[row][col]['text'] = self.turn
            self.buttons[row][col]['bg'] = "lightgreen" if self.turn == "X" else "lightcoral"
            self.board[row][col] = self.turn
            self.moves_count += 1

            if self.check_winner(row, col):
                self.declare_winner(self.turn)
            elif self.moves_count == self.size**2:
                self.declare_draw()
            else:
                self.turn = "O" if self.turn == "X" else "X"

    def check_winner(self, row, col):
        # Check row
        if all(self.board[row][c] == self.turn for c in range(self.size)):
            return True
            
        # Check column
        if all(self.board[r][col] == self.turn for r in range(self.size)):
            return True
            
        # Check main diagonal
        if row == col:
            if all(self.board[i][i] == self.turn for i in range(self.size)):
                return True
                
        # Check anti-diagonal
        if row + col == self.size - 1:
            if all(self.board[i][self.size-1-i] == self.turn for i in range(self.size)):
                return True
                
        return False

    def declare_winner(self, player):
        self.winner_declared = True
        self.winner = f"Player {player}"
        self.home_page()

    def declare_draw(self):
        self.winner_declared = True
        self.home_page()

if __name__ == "__main__":
    root = tk.Tk()
    game = TicTacToe(root)
    root.mainloop()
