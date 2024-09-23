# player.py


class Player:
    def __init__(self, name):
        """
        Initialize a new player with a name.
        """
        self.name = name
        self.score = 0
        self.skip_turns = 0  # Number of "Skip Turn" tokens the player has
        self.score_history = []  # To track score progression over turns

    def add_score(self, points):
        """
        Add points to the player's score and record the new score in history.
        """
        self.score += points
        self.score_history.append(self.score)

    def use_skip_turn(self):
        """
        Use a "Skip Turn" token if available.
        Returns True if the token was used, False otherwise.
        """
        if self.skip_turns > 0:
            self.skip_turns -= 1
            return True
        return False

    def add_skip_turn(self):
        """
        Add a "Skip Turn" token to the player's inventory.
        """
        self.skip_turns += 1

    def reset(self):
        """
        Reset the player's score and skip turns for a new game.
        """
        self.score = 0
        self.skip_turns = 0
        self.score_history = []

    def __str__(self):
        return (
            f"Player({self.name}, Score: {self.score}, Skip Turns: {self.skip_turns})"
        )
