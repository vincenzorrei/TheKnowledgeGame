# game.py

import random
import tkinter as tk
from tkinter import messagebox, simpledialog

from packages.chart import Chart
from packages.excel_reader import ExcelReader
from packages.player import Player
from packages.question import Question
from packages.sound_manager import SoundManager
from packages.timer import Timer


class Game:
    def __init__(self, root):
        """
        Initialize the game with the main Tkinter window.
        """
        self.root = root
        self.players = []
        self.current_player_index = 0
        self.questions = []
        self.current_question = None
        self.sound_manager = SoundManager()
        self.timer = None
        self.reading_time = 0
        self.answer_time = 0
        self.is_challenge = False
        self.probability_of_event = 0.3  # Adjust as needed
        self.rounds_completed = 0

        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements.
        """
        self.root.geometry("600x400")

        self.name_label = tk.Label(
            self.root, text="Enter player names (comma-separated):"
        )
        self.name_label.pack()

        self.name_entry = tk.Entry(self.root)
        self.name_entry.pack()

        self.start_button = tk.Button(
            self.root, text="Start Game", command=self.start_game
        )
        self.start_button.pack()

        self.question_label = tk.Label(self.root, text="", wraplength=500)
        self.answer_entry = tk.Entry(self.root)
        self.submit_button = tk.Button(
            self.root, text="Submit Answer", command=self.submit_answer
        )

    def start_game(self):
        """
        Start the game after collecting player names.
        """
        names = self.name_entry.get().split(",")
        if not names:
            messagebox.showerror("Error", "Please enter at least one player name.")
            return

        self.players = [Player(name.strip()) for name in names if name.strip()]
        if not self.players:
            messagebox.showerror("Error", "Please enter valid player names.")
            return

        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()

        # Load questions from Excel
        excel_reader = ExcelReader("questions.xlsx")
        self.questions = excel_reader.load_questions()

        self.next_turn()

    def next_turn(self):
        """
        Proceed to the next player's turn.
        """
        # Check if all questions have been asked
        if all(q.asked for q in self.questions):
            self.end_game()
            return

        # Check if we need to ask players whether to continue
        if self.current_player_index == 0 and self.rounds_completed > 0:
            continue_game = messagebox.askyesno(
                "Continue Game", "Do you want to play another round?"
            )
            if not continue_game:
                self.end_game()
                return

        self.current_player = self.players[self.current_player_index]
        self.opponent_player = None

        # Check if the current player is skipped
        if self.current_player.skip_turns > 0:
            self.current_player.skip_turns -= 1
            messagebox.showinfo(
                "Skip Turn", f"{self.current_player.name}'s turn is skipped!"
            )
            self.sound_manager.play_skip_sound()
            self.advance_player()
            self.next_turn()
            return

        self.offer_question()

    def offer_question(self):
        """
        Offer a question to the player by showing the domain and difficulty.
        The player can choose to accept or re-draw.
        """
        unasked_questions = [q for q in self.questions if not q.asked]
        if not unasked_questions:
            self.end_game()
            return

        self.current_question = random.choice(unasked_questions)

        # Show domain and difficulty
        domain = self.current_question.domain
        difficulty = self.current_question.difficulty

        accept = messagebox.askyesno(
            "Question Offer",
            f"{self.current_player.name}, your question is from the domain '{domain}' with difficulty level {difficulty}.\nDo you accept this question?",
        )

        if accept:
            self.current_question.asked = True
            self.display_question()
        else:
            # Re-draw a different question
            self.offer_question()

    def display_question(self):
        """
        Display the current question to the player.
        """
        self.question_label.config(
            text=f"{self.current_player.name}, here is your question:\n\n{self.current_question.text}"
        )
        self.question_label.pack()

        # Calculate timers
        word_count = len(self.current_question.text.split())
        self.reading_time = word_count * 0.3
        self.answer_time = self.current_question.difficulty * 45

        if self.is_challenge:
            self.answer_time = self.current_question.difficulty * 90

        # Start the reading timer
        self.timer = Timer(self.root, self.reading_time, self.start_answer_timer)
        self.timer.start()

    def start_answer_timer(self):
        """
        Start the timer for answering the question.
        """

        self.submit_button.pack()

        self.timer = Timer(self.root, self.answer_time, self.time_up)
        self.timer.start()

    def submit_answer(self):
        """
        Handle the submission of an answer.
        """
        self.timer.cancel()
        self.submit_button.pack_forget()

        # Ask the user to confirm if the answer is correct
        is_correct = messagebox.askyesno(
            "Answer Confirmation", "Is the answer correct?"
        )
        if is_correct and not self.is_challenge:
            points = self.current_question.difficulty
            # Double points if answered before time runs out
            if self.timer.time_remaining > 0:
                points *= 2
            self.current_player.add_score(points)
            self.sound_manager.play_correct_sound()

            # Random event: Challenge or Skip Turn
            event_chance = random.random()
            if event_chance < self.probability_of_event:
                self.handle_random_event()

        elif is_correct and self.is_challenge:
            points = self.current_question.difficulty * 2
            self.current_player.add_score(points)
            self.opponent_player.add_score(-points)
            self.sound_manager.play_correct_sound()

        else:
            self.sound_manager.play_incorrect_sound()

        self.advance_player()
        self.next_turn()

    def time_up(self):
        """
        Handle the event when the time is up.
        """
        messagebox.showinfo("Time's Up", "You ran out of time!")
        self.answer_entry.pack_forget()
        self.submit_button.pack_forget()
        self.sound_manager.play_time_up_sound()

        self.advance_player()
        self.next_turn()

    def handle_random_event(self):
        """
        Handle random events like Challenge or Skip Turn.
        """
        event = random.choice(["challenge", "skip_turn"])
        if event == "challenge":
            self.sound_manager.play_challenge_sound()
            opponent = self.select_opponent()
            if opponent:
                messagebox.showinfo(
                    "Challenge", f"You are challenging {opponent.name}!"
                )
                self.is_challenge = True
                # Swap the current player to the opponent
                self.opponent_player = opponent
                self.display_question()

        elif event == "skip_turn":
            self.sound_manager.play_skip_sound()
            opponent = self.select_opponent()
            if opponent:
                opponent.add_skip_turn()
                messagebox.showinfo(
                    "Skip Turn", f"{opponent.name} will skip their next turn!"
                )

    def select_opponent(self):
        """
        Allow the player to select an opponent.
        """
        opponent_names = [p.name for p in self.players if p != self.current_player]
        if not opponent_names:
            return None

        opponent_name = simpledialog.askstring(
            "Select Opponent", f"Choose an opponent: {', '.join(opponent_names)}"
        )
        for player in self.players:
            if player.name == opponent_name:
                return player
        return None

    def advance_player(self):
        """
        Advance to the next player.
        """
        prev_player_index = self.current_player_index
        self.current_player_index = (self.current_player_index + 1) % len(self.players)
        self.is_challenge = False

        if (
            self.current_player_index == 0
            and prev_player_index != self.current_player_index
        ):
            # A full round is completed
            self.rounds_completed += 1

    def end_game(self):
        """
        Handle the end of the game.
        """
        # Destroy the root window to terminate the Tkinter main loop
        self.root.destroy()
        # Show the score chart after Tkinter has been closed
        Chart.show_score_chart(self.players)
