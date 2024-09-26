# game.py

import random
from tkinter import simpledialog

import customtkinter as ctk
from CTkMessagebox import CTkMessagebox

from packages.chart import Chart
from packages.excel_reader import ExcelReader
from packages.player import Player
from packages.question import Question
from packages.sound_manager import SoundManager
from packages.timer import Timer


class Game:
    def __init__(self, root):
        """
        Initialize the game with the main customtkinter window.
        """
        self.root = root
        ctk.set_appearance_mode("System")  # Modes: "System" (default), "Dark", "Light"
        ctk.set_default_color_theme(
            "blue"
        )  # Themes: "blue" (default), "green", "dark-blue"

        self.players = []
        self.current_player_index = 0
        self.current_player = None  # Initialize current_player
        self.questions = []
        self.current_question = None
        self.sound_manager = SoundManager()
        self.timer = None
        self.reading_time = 0
        self.answer_time = 0
        self.is_challenge = False
        self.opponent_player = None  # Store the selected opponent
        self.probability_of_event = 0.8  # Adjust as needed
        self.rounds_completed = 0

        self.setup_ui()

    def setup_ui(self):
        """
        Set up the user interface elements using customtkinter.
        """
        self.root.geometry("800x600")
        self.root.title("Quiz Game")

        self.main_frame = ctk.CTkFrame(self.root)
        self.main_frame.pack(pady=20, padx=20, fill="both", expand=True)

        self.name_label = ctk.CTkLabel(
            self.main_frame,
            text="Enter player names (comma-separated):",
            font=ctk.CTkFont(size=14),
        )
        self.name_label.pack(pady=12)

        self.name_entry = ctk.CTkEntry(self.main_frame, width=400)
        self.name_entry.pack(pady=12)

        self.start_button = ctk.CTkButton(
            self.main_frame, text="Start Game", command=self.start_game
        )
        self.start_button.pack(pady=12)

        # Create a frame for the question and timer
        self.question_frame = ctk.CTkFrame(self.root)
        self.question_label = ctk.CTkLabel(
            self.question_frame,
            text="",
            font=ctk.CTkFont(size=18),
            wraplength=500,
            justify="left",
        )
        self.timer_label = ctk.CTkLabel(
            self.question_frame,
            text="",
            fg_color="transparent",
            text_color="red",
            font=ctk.CTkFont(size=14),
        )

        # Place the question label in the frame; timer_label will be packed when needed
        self.question_label.pack(pady=10)

        # Reference timer_label in root so Timer can access it
        self.root.timer_label = self.timer_label

        self.submit_button = ctk.CTkButton(
            self.root, text="Submit Answer", command=self.submit_answer
        )

        # Sidebar Frame (Do not pack yet)
        self.sidebar_frame = ctk.CTkFrame(self.root, width=200)
        # self.sidebar_frame.pack(side="right", fill="y")  # Move this to start_game()

        # Top Players Section
        self.top_players_frame = ctk.CTkFrame(self.sidebar_frame)
        self.top_players_frame.pack(pady=10, padx=10, fill="x")

        self.top_players_label = ctk.CTkLabel(
            self.top_players_frame,
            text="Top Players",
            font=ctk.CTkFont(size=14, weight="bold"),
        )
        self.top_players_label.pack(pady=(10, 5))

        self.top_players_text = ctk.CTkLabel(
            self.top_players_frame, text="", font=ctk.CTkFont(size=12), justify="left"
        )
        self.top_players_text.pack(pady=5)

        # Separator
        separator1 = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray")
        separator1.pack(fill="x", pady=10)

        # Rounds Completed Section
        self.rounds_frame = ctk.CTkFrame(self.sidebar_frame)
        self.rounds_frame.pack(pady=10, padx=10, fill="x")

        self.rounds_label = ctk.CTkLabel(
            self.rounds_frame,
            text="Rounds Completed",
            font=ctk.CTkFont(size=14, weight="bold"),
        )

        self.rounds_label.pack(pady=(10, 5))

        self.rounds_text = ctk.CTkLabel(
            self.rounds_frame, text="0", font=ctk.CTkFont(size=12)
        )
        self.rounds_text.pack(pady=5)

        # Separator
        separator2 = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray")
        separator2.pack(fill="x", pady=10)

        # Current Player Section
        self.current_player_frame = ctk.CTkFrame(self.sidebar_frame)
        self.current_player_frame.pack(pady=10, padx=10, fill="x")

        self.current_player_label = ctk.CTkLabel(
            self.current_player_frame,
            text="Current Player",
            font=ctk.CTkFont(size=14, weight="bold"),
        )

        self.current_player_label.pack(pady=(10, 5))

        self.current_player_text = ctk.CTkLabel(
            self.current_player_frame,
            text="",
            font=ctk.CTkFont(size=12),
        )
        self.current_player_text.pack(pady=5)

        # Separator
        separator3 = ctk.CTkFrame(self.sidebar_frame, height=2, fg_color="gray")
        separator3.pack(fill="x", pady=10)

        # Question Info Section
        self.question_info_frame = ctk.CTkFrame(self.sidebar_frame)
        self.question_info_frame.pack(pady=10, padx=10, fill="x")

        self.question_info_label = ctk.CTkLabel(
            self.question_info_frame,
            text="Question Info",
            font=ctk.CTkFont(size=14, weight="bold"),
        )

        self.question_info_label.pack(pady=(10, 5))

        self.question_info_text = ctk.CTkLabel(
            self.question_info_frame, text="", font=ctk.CTkFont(size=12), justify="left"
        )

        self.question_info_text.pack(pady=5)

    def update_sidebar(self):
        """
        Update the sidebar with current game information.
        """
        # Update top players
        sorted_players = sorted(self.players, key=lambda p: p.score, reverse=True)
        top_players = sorted_players[:3]
        top_players_text = "\n".join(
            [
                f"{i+1}. {player.name}: {player.score}"
                for i, player in enumerate(top_players)
            ]
        )
        self.top_players_text.configure(text=top_players_text)

        # Update rounds completed
        self.rounds_text.configure(text=f"{self.rounds_completed}")

        # Update current player
        if self.current_player:
            self.current_player_text.configure(text=f"{self.current_player.name}")
        else:
            self.current_player_text.configure(text="")

        # Update question info
        if self.current_question:
            domain = self.current_question.domain
            difficulty = self.current_question.difficulty
            difficulty_str = "*" * int(difficulty)
            self.question_info_text.configure(
                text=f"Domain: {domain}\nDifficulty: {difficulty_str}"
            )
        else:
            self.question_info_text.configure(text="")

    def start_game(self):
        """
        Start the game after collecting the player names.
        """
        names = self.name_entry.get().split(",")
        if not names:
            CTkMessagebox(
                title="Errore",
                message="Per favore inserisci almeno un nome di giocatore.",
                icon="cancel",
            ).get()
            return

        self.players = [Player(name.strip()) for name in names if name.strip()]
        if not self.players:
            CTkMessagebox(
                title="Errore",
                message="Per favore inserisci nomi di giocatori validi.",
                icon="cancel",
            ).get()
            return

        self.name_label.pack_forget()
        self.name_entry.pack_forget()
        self.start_button.pack_forget()
        self.main_frame.pack_forget()

        # Load questions from Excel
        excel_reader = ExcelReader("questions.xlsx")
        self.questions = excel_reader.load_questions()

        # Show the menu for selecting domains and difficulty
        self.show_domain_difficulty_menu()

    def show_domain_difficulty_menu(self):
        """
        Display a menu to select domains and the minimum difficulty level.
        """
        # Get the list of unique domains from the questions
        domains = sorted(set(q.domain for q in self.questions))

        # Create a new Toplevel window
        self.settings_window = ctk.CTkToplevel(self.root)
        self.settings_window.title("Impostazioni del Gioco")
        self.settings_window.geometry("400x400")
        self.settings_window.grab_set()  # Make the window modal

        # Section for domain selection
        domain_label = ctk.CTkLabel(
            self.settings_window,
            text="Seleziona i Domini da Includere:",
            font=ctk.CTkFont(size=14),
        )
        domain_label.pack(pady=(20, 10))

        # Create checkboxes for each domain
        self.domain_vars = {}
        for domain in domains:
            var = ctk.BooleanVar(value=True)
            chk = ctk.CTkCheckBox(self.settings_window, text=domain, variable=var)
            chk.pack(anchor="w", padx=20)
            self.domain_vars[domain] = var

        # Section for selecting minimum difficulty
        difficulty_label = ctk.CTkLabel(
            self.settings_window,
            text="Seleziona il Livello Minimo di Difficoltà:",
            font=ctk.CTkFont(size=14),
        )
        difficulty_label.pack(pady=(20, 10))

        # Difficulty options (assuming difficulty levels are integers)
        difficulties = sorted(set(int(q.difficulty) for q in self.questions))
        self.min_difficulty_var = ctk.IntVar(value=min(difficulties))

        # Create an OptionMenu for difficulty selection
        difficulty_menu = ctk.CTkOptionMenu(
            self.settings_window,
            values=[str(d) for d in difficulties],
            variable=self.min_difficulty_var,
        )
        difficulty_menu.pack(pady=10)

        # Button to start the game
        start_game_button = ctk.CTkButton(
            self.settings_window,
            text="Avvia il Gioco",
            command=self.apply_settings_and_start_game,
        )
        start_game_button.pack(pady=20)

    def apply_settings_and_start_game(self):
        """
        Apply the selected settings and start the game.
        """
        # Get the selected domains
        selected_domains = [
            domain for domain, var in self.domain_vars.items() if var.get()
        ]
        if not selected_domains:
            CTkMessagebox(
                title="Errore",
                message="Per favore seleziona almeno un dominio.",
                icon="warning",
            ).get()
            return

        # Get the minimum difficulty
        min_difficulty = self.min_difficulty_var.get()

        # Filter questions based on selected domains and minimum difficulty
        self.questions = [
            q
            for q in self.questions
            if q.domain in selected_domains and int(q.difficulty) >= min_difficulty
        ]
        if not self.questions:
            CTkMessagebox(
                title="Errore",
                message="Nessuna domanda corrisponde ai criteri selezionati.",
                icon="warning",
            ).get()
            return

        # Close the settings window
        self.settings_window.destroy()

        # Pack the sidebar frame
        self.sidebar_frame.pack(side="right", fill="y")

        # Proceed to the first turn
        self.next_turn()

    def next_turn(self):
        """
        Proceed to the next player's turn.
        """
        # Reset opponent_player at the start of the turn
        self.opponent_player = None

        # Assign current player
        self.current_player = self.players[self.current_player_index]

        # Update sidebar
        self.update_sidebar()

        # Check if all questions have been asked
        if all(q.asked for q in self.questions):
            self.end_game()
            return

        # Check if we need to ask players whether to continue
        if self.current_player_index == 0 and self.rounds_completed > 0:
            continue_game = CTkMessagebox(
                title="Continue Game",
                message="Do you want to play another round?",
                icon="question",
                option_1="No",
                option_2="Yes",
            ).get()
            if continue_game == "No":
                self.end_game()
                return

        # Check if the current player is skipped
        if self.current_player.skip_turns > 0:
            self.current_player.skip_turns -= 1
            self.sound_manager.play_skip_sound()
            CTkMessagebox(
                title="Skip Turn",
                message=f"{self.current_player.name}'s turn is skipped!",
                icon="info",
            ).get()
            self.advance_player()
            self.next_turn()
            return

        self.offer_question()

    def choose_unasked_question(self):
        """
        Choose an unasked question randomly.
        """
        unasked_questions = [q for q in self.questions if not q.asked]
        if not unasked_questions:
            self.end_game()
            return

        return random.choice(unasked_questions)

    def offer_question(self):
        """
        Offer a question to the player by showing the domain and difficulty.
        The player can choose to accept or re-draw.
        """
        # Hide previous question and timer
        self.question_frame.pack_forget()
        self.timer_label.pack_forget()
        self.timer_label.configure(text="")
        self.question_label.configure(text="")
        self.submit_button.pack_forget()

        self.current_question = self.choose_unasked_question()

        # Show domain and difficulty
        domain = self.current_question.domain
        difficulty = self.current_question.difficulty
        difficulty_str = "*" * int(difficulty)

        if not self.is_challenge:
            accept = CTkMessagebox(
                title=f"Question Offer for {self.current_player.name}",
                message=f"{self.current_player.name}\n\nDomain: {domain}\nDifficulty level: {difficulty_str}\n\nDo you accept?",
                icon="question",
                icon_size=(20, 20),
                option_1="No",
                option_2="Yes",
            ).get()
            accept = accept == "Yes"
        else:
            CTkMessagebox(
                title=f"Question Offer for {self.current_player.name}",
                message=f"{self.current_player.name}\n\nDomain: {domain}\nDifficulty level: {difficulty_str}",
                icon="info",
                icon_size=(20, 20),
            ).get()
            accept = True

        if accept:
            self.current_question.asked = True
            self.update_sidebar()
            self.display_question()
        else:
            # Re-draw a different question
            self.offer_question()

    def display_question(self):
        """
        Display the current question to the player.
        """
        # Cancel any existing timer
        if self.timer:
            self.timer.cancel()
            self.timer = None

        self.question_label.configure(
            text=f"{self.current_player.name}, here is your question:\n\n{self.current_question.text}"
        )
        self.timer_label.configure(text="")  # Reset timer label text

        # Pack the question frame
        self.question_frame.pack(pady=20, padx=20, fill="both", expand=True)

        # Remove the submit button if it is visible
        self.submit_button.pack_forget()

        # Calculate timers
        word_count = len(self.current_question.text.split())
        self.reading_time = word_count * 0.3
        self.answer_time = self.current_question.difficulty * 45

        if self.is_challenge:
            self.answer_time = self.current_question.difficulty * 60
            self.sound_manager.play_challenge_suspance_sound()

        # Start the reading timer
        self.timer = Timer(self.root, self.reading_time, self.start_answer_timer)
        self.timer.start()

    def start_answer_timer(self):
        """
        Start the timer for answering the question.
        """
        # Cancel any existing timer
        if self.timer:
            self.timer.cancel()
            self.timer = None

        # Keep the question text displayed
        # Pack the timer_label to show the timer
        self.timer_label.pack()

        self.submit_button.pack(pady=10)

        # Start the answer timer
        self.timer = Timer(self.root, self.answer_time, self.time_up)
        self.timer.start()

    def submit_answer(self):
        """
        Handle the submission of an answer.
        """
        time_remaining = self.timer.time_remaining if self.timer else 0
        if self.timer:
            self.timer.cancel()
            self.timer = None
        self.submit_button.pack_forget()
        # Hide the timer_label and question_frame
        self.timer_label.pack_forget()
        self.question_frame.pack_forget()

        # Ask the user to confirm if the answer is correct
        is_correct = (
            CTkMessagebox(
                title="Answer Confirmation",
                message="Is the answer correct?",
                icon="question",
                option_1="No",
                option_2="Yes",
            ).get()
            == "Yes"
        )

        if is_correct:
            if self.is_challenge:
                # Challenge: Current player gains points; opponent loses points
                points = self.current_question.difficulty
                if time_remaining <= 0:
                    points = 0
                self.current_player.add_score(points)
                if self.opponent_player:
                    self.opponent_player.add_score(-points)
                self.sound_manager.play_correct_sound()
            else:
                # Regular question
                points = self.current_question.difficulty
                # Double points if answered before time runs out
                if time_remaining > 0:
                    points *= 2
                self.current_player.add_score(points)
                self.sound_manager.play_correct_sound()

                # Random event: Challenge or Skip Turn
                event_chance = random.random()
                if event_chance < self.probability_of_event:
                    self.handle_random_event()
                    if self.is_challenge:
                        return  # Exit early to handle the challenge
                    # For skip_turn, continue to advance_player()
        else:
            self.sound_manager.play_incorrect_sound()

        # Reset challenge flag and opponent after handling
        self.is_challenge = False
        self.opponent_player = None

        self.update_sidebar()
        self.advance_player()
        self.next_turn()

    def time_up(self):
        """
        Handle the event when the answer time is up.
        """
        if self.is_challenge:
            # For challenges, time up means the answer is incorrect
            CTkMessagebox(
                title="Time's Up",
                message="Time is up! The answer is considered incorrect.",
                icon="warning",
            ).get()
            self.submit_button.pack_forget()
            self.timer_label.pack_forget()
            self.question_frame.pack_forget()
            self.sound_manager.play_time_up_sound()

            # Proceed as if the answer was incorrect
            self.sound_manager.play_incorrect_sound()
            # Reset challenge flag and opponent
            self.is_challenge = False
            self.opponent_player = None
            # Advance to next player
            self.advance_player()
            self.next_turn()
        else:
            # For regular questions, nothing happens; player can still submit the answer
            self.timer_label.configure(
                text="Time's up! You can still submit your answer."
            )
            # Cancel the timer to prevent further updates
            if self.timer:
                self.timer.cancel()
                self.timer = None

    def handle_random_event(self):
        """
        Handle random events like Challenge or Skip Turn.
        """
        event = random.choice(["challenge", "skip_turn"])
        if event == "challenge":
            self.sound_manager.play_challenge_sound()
            opponent = self.select_opponent()
            if opponent:
                self.opponent_player = opponent
                self.is_challenge = True
                # CTkMessagebox(
                #     title="Challenge",
                #     message=f"You are challenging {opponent.name}!",
                #     icon="info",
                # )

                # Reset the timer before starting the challenge
                if self.timer:
                    self.timer.cancel()
                    self.timer = None
                self.offer_question()
        elif event == "skip_turn":
            self.sound_manager.choose_player_to_skip_sound()
            opponent = self.select_opponent(event="skip_turn")
            if opponent:
                opponent.add_skip_turn()

            # Do not return or call advance_player here; let submit_answer handle it

    def select_opponent(self, event="challenge"):
        """
        Allow the current player to select an opponent.

        Returns:
            Player: The selected opponent, or None if selection is canceled.
        """

        # Create a new Toplevel window
        opponent_names = [p.name for p in self.players if p != self.current_player]
        if not opponent_names:
            return None

        title = "Challenge"
        text = "Choose an opponent:"
        if event == "skip_turn":
            title = "Skip Turn"
            text = "Select a player to skip his turn:"

        # Create a new Toplevel window
        dialog = ctk.CTkToplevel(self.root)
        dialog.title(title)
        dialog.geometry("300x200")
        dialog.grab_set()  # Make the dialog modal

        label = ctk.CTkLabel(dialog, text=text, font=ctk.CTkFont(size=14))
        label.pack(pady=10)

        # Variable to store the selected opponent
        selected_opponent = ctk.StringVar(value=opponent_names[0])

        # Create OptionMenu for opponent selection
        opponent_menu = ctk.CTkOptionMenu(
            dialog, values=opponent_names, variable=selected_opponent
        )
        opponent_menu.pack(pady=10)

        def on_confirm():
            dialog.destroy()

        confirm_button = ctk.CTkButton(dialog, text="Confirm", command=on_confirm)
        confirm_button.pack(pady=10)

        self.root.wait_window(dialog)  # Wait until the dialog is closed

        opponent_name = selected_opponent.get()

        for player in self.players:
            if player.name == opponent_name:
                return player

        CTkMessagebox(
            title="Invalid Selection",
            message="Please select a valid opponent.",
            icon="warning",
        ).get()
        return self.select_opponent()

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
        # Destroy the root window to terminate the customtkinter main loop
        self.root.destroy()
        # Show the score chart after customtkinter has been closed
        Chart.show_score_chart(self.players)


if __name__ == "__main__":
    app = ctk.CTk()
    game = Game(app)
    app.mainloop()
