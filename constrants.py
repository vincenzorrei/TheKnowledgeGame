# constants.py

# Timing constants
READING_TIME_MULTIPLIER = 0.3  # Seconds per word for reading time
ANSWER_TIME_MULTIPLIER = 45  # Seconds per difficulty level for answering time
CHALLENGE_ANSWER_TIME_MULTIPLIER = (
    90  # Seconds per difficulty level for challenge answering time
)

# Probability settings
PROBABILITY_OF_EVENT = (
    0.5  # Probability of triggering a special event after a correct answer
)

# Maximum retries
MAX_RETRIES_FOR_QUESTION = 3  # Maximum times a player can re-draw a question

# Sound file paths
SOUND_FILE_PATHS = {
    "correct": "sounds/correct.wav",
    "incorrect": "sounds/incorrect.wav",
    "time_up": "sounds/time_up.wav",
    "challenge": "sounds/challenge.wav",
    "skip": "sounds/skip.wav",
}

# Excel file path
EXCEL_FILE_PATH = "questions.xlsx"
