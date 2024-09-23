# question.py


class Question:
    def __init__(self, text, domain, difficulty):
        """
        Initialize a Question object.

        Args:
            text (str): The text of the question.
            domain (str): The domain or category of the question.
            difficulty (int): The difficulty level of the question.
        """
        self.text = text
        self.domain = domain
        self.difficulty = difficulty
        self.asked = False  # Indicates whether the question has been asked

    def __str__(self):
        """
        Return a string representation of the Question object.
        """
        return f"Question(Domain: {self.domain}, Difficulty: {self.difficulty}, Text: {self.text[:100]}...)"
