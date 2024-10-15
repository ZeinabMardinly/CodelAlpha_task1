import random
import tkinter as tk
from tkinter import messagebox

# Dictionary of words by category
words = {
    "fruits": ["pineapple", "strawberry", "banana", "watermelon", "grapefruit"],
    "animals": ["elephant", "giraffe", "butterfly", "crocodile", "kangaroo"],
    "technology": ["python", "algorithm", "computer", "spaceship", "robot"],
    "nature": ["waterfall", "volcano", "avalanche", "hurricane", "mountain"]
}

# Dictionary of hangman stages
hangman = {
    0: ("  ",
        "  ",
        "  "),
    1: (" o ",
        "   ",
        "   "),
    2: (" o ",
        " | ",
        "   "),
    3: (" o ",
        " |\\",
        "   "),
    4: (" o ",
        "/|\\",
        "   "),
    5: (" o ",
        "/|\\",
        "/  "),
    6: (" o ",
        "/|\\",
        "/ \\")
}

class HangmanGame:
    def __init__(self, root):
        self.root = root
        self.root.title("Hangman Game")

        self.canvas = tk.Canvas(root, width=300, height=250)
        self.canvas.pack()

        self.hint_label = tk.Label(root, text="", font=("Arial", 24))
        self.hint_label.pack()

        self.entry = tk.Entry(root)
        self.entry.pack()

        self.guess_button = tk.Button(root, text="Guess", command=self.check_guess)
        self.guess_button.pack()

        self.reset_button = tk.Button(root, text="New Game", command=self.start_game)
        self.reset_button.pack()

        self.category_button = tk.Button(root, text="Select Category", command=self.select_category)
        self.category_button.pack()

        self.wrong_guesses = 0
        self.guesses_letters = set()
        self.answer = ""
        self.hint = []
        self.selected_category = ""

        self.start_game()

    def select_category(self):
        category_window = tk.Toplevel(self.root)
        category_window.title("Select Category")
        tk.Label(category_window, text="Choose a category:").pack()

        for category in words.keys():
            tk.Button(category_window, text=category.capitalize(), command=lambda c=category: self.set_category(c, category_window)).pack()

    def set_category(self, category, window):
        self.selected_category = category
        window.destroy()  
        self.start_game()

    def start_game(self):
        if not self.selected_category:
            messagebox.showwarning("Select Category", "Please select a category first.")
            return
        self.answer = random.choice(words[self.selected_category])
        self.hint = ["_"] * len(self.answer)
        self.wrong_guesses = 0
        self.guesses_letters.clear()
        self.update_display()

    def update_display(self):
        self.canvas.delete("all")

        y_position = 40
        for line in hangman[self.wrong_guesses]:
            self.canvas.create_text(150, y_position, text=line, font=("Arial", 20))
            y_position += 20  

        
        self.hint_label.config(text=" ".join(self.hint))

    def check_guess(self):
        guess = self.entry.get().lower()
        self.entry.delete(0, tk.END)

        if len(guess) != 1 or not guess.isalpha():
            messagebox.showwarning("Invalid Input", "Please enter a single letter.")
            return

        if guess in self.guesses_letters:
            messagebox.showwarning("Already Guessed", f"{guess} has already been guessed.")
            return

        self.guesses_letters.add(guess)

        if guess in self.answer:
            for i in range(len(self.answer)):
                if self.answer[i] == guess:
                    self.hint[i] = guess
        else:
            self.wrong_guesses += 1

        self.update_display()

        if "_" not in self.hint:
            messagebox.showinfo("You Win!", "Congratulations! You Win!")
            self.selected_category = ""  
            self.start_game()
        elif self.wrong_guesses >= len(hangman) - 1:
            messagebox.showinfo("You Lose!", f"The correct word was: {self.answer}")
            self.selected_category = ""  
            self.start_game()

if __name__ == "__main__":
    root = tk.Tk()
    game = HangmanGame(root)
    root.mainloop()
