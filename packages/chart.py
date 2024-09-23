# chart.py

import matplotlib.pyplot as plt

from packages.player import Player


class Chart:
    @staticmethod
    def show_score_chart(players):
        """
        Display a line chart showing each player's score progression over the game turns.

        Args:
            players (List[Player]): A list of Player objects.
        """
        plt.figure(figsize=(10, 6))
        max_turns = max(len(player.score_history) for player in players)
        turns = range(1, max_turns + 1)

        for player in players:
            # Extend the player's score history if necessary
            score_history = player.score_history
            if len(score_history) < max_turns:
                score_history += [score_history[-1]] * (max_turns - len(score_history))
            plt.plot(turns, score_history, marker="o", label=player.name)

        plt.title("Score Progression Over Turns")
        plt.xlabel("Turn Number")
        plt.ylabel("Score")
        plt.legend()
        plt.grid(True)
        plt.tight_layout()
        plt.show()
