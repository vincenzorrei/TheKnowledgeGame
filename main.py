import tkinter as tk

from packages.game import Game


def main():
    root = tk.Tk()
    root.title("Quiz Game")
    game = Game(root)
    root.mainloop()


if __name__ == "__main__":
    main()
