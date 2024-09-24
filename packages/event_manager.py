# # event_manager.py

# import random
# from tkinter import messagebox, simpledialog

# from packages.sound_manager import SoundManager


# class EventManager:
#     def __init__(self, game):
#         """
#         Initialize the EventManager with a reference to the Game instance.

#         Args:
#             game (Game): The instance of the Game class.
#         """
#         self.game = game
#         self.sound_manager = SoundManager()
#         self.probability_of_event = 0.5  # Adjust as needed

#     def check_for_event(self):
#         """
#         Determine if a random event should occur based on probability.
#         """
#         event_chance = random.random()
#         if event_chance < self.probability_of_event:
#             self.trigger_random_event()

#     def trigger_random_event(self):
#         """
#         Trigger a random event: either 'challenge' or 'skip_turn'.
#         """
#         event = random.choice(["challenge", "skip_turn"])
#         if event == "challenge":
#             self.handle_challenge_event()
#         elif event == "skip_turn":
#             self.handle_skip_turn_event()

#     def handle_challenge_event(self):
#         """
#         Handle the 'Challenge an Opponent' event.
#         """
#         self.sound_manager.play_challenge_sound()
#         opponent = self.select_opponent()
#         if opponent:
#             messagebox.showinfo("Challenge", f"You are challenging {opponent.name}!")
#             self.game.is_challenge = True
#             # Swap the current player to the opponent for the challenge
#             self.game.current_player = opponent
#             self.game.offer_question()  # Offer a question to the opponent

#     def handle_skip_turn_event(self):
#         """
#         Handle the 'Skip Opponent's Turn' event.
#         """
#         self.sound_manager.play_skip_sound()
#         opponent = self.select_opponent()
#         if opponent:
#             opponent.add_skip_turn()
#             messagebox.showinfo(
#                 "Skip Turn", f"{opponent.name} will skip their next turn!"
#             )

#     # def select_opponent(self):
#     #     """
#     #     Allow the current player to select an opponent.

#     #     Returns:
#     #         Player: The selected opponent, or None if selection is canceled.
#     #     """
#     #     opponent_names = [
#     #         p.name for p in self.game.players if p != self.game.current_player
#     #     ]
#     #     if not opponent_names:
#     #         return None

#     #     # Create a dictionary with integer keys for the opponent names so that the player can select an opponent by entering the corresponding number.
#     #     opponent_dict = {i + 1: name for i, name in enumerate(opponent_names)}
#     #     opponent_key = simpledialog.askinteger(
#     #         "Select Opponent",
#     #         f"Choose an opponent:\n{'\n'.join(f'{k}: {v}' for k, v in opponent_dict.items())}",
#     #         minvalue=1,
#     #         maxvalue=len(opponent_dict),
#     #     )
#     #     opponent_name = opponent_dict.get(opponent_key)

#     #     if opponent_name in opponent_names:
#     #         for player in self.game.players:
#     #             if player.name == opponent_name:
#     #                 return player

#     #     else:
#     #         messagebox.showerror("Invalid Selection", "Please select a valid opponent.")
#     #         return self.select_opponent()
# \n{self.current_player} gains {points} points!\n{self.opponent_player} loses {points} points!
