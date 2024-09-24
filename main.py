# main.py

import customtkinter as ctk

from packages.game import Game


def main():
    app = ctk.CTk()
    app.title("The Data Game")
    game = Game(app)
    app.mainloop()


if __name__ == "__main__":
    main()
