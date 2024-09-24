# The Knowledge Game
A Python-based interactive quiz game with multiplayer support, developed using Tkinter for the GUI. Players answer questions from various domains and difficulties, with random events like challenges and skip turns to spice up the gameplay.

## Table of Contents
- Features
- Requirements
- Installation
- How to Run
- Gameplay Instructions
- Contributing
- License

## Features
Multiplayer Support: Add multiple players to compete in the quiz.
Randomized Questions: Questions are loaded from an Excel file and presented randomly.
Timed Questions: Players have limited time to read and answer each question.
Challenges: Random events allow players to challenge others, adding strategic depth.
Skip Turns: Players can force opponents to skip their next turn.
Score Tracking: Scores are calculated based on question difficulty and time taken.
Score Chart: At the end of the game, a score chart is displayed showing the progression.

## Requirements
Python 3.x
Tkinter (usually included with Python)
Required Python Packages:
pandas
matplotlib
openpyxl
Note: The winsound module used for sound effects is only available on Windows and does not require installation.

## Installation
Clone the Repository

```console
git clone https://github.com/vincenzorrei/TheKnowledgeGame.git
```

Install the required Python packages using pip:

```console
pip install -r requirements.txt
```


## How to Run
To obtain the dataset of questions and the two reference datasets to complete the exercises, please send an email to vin.orrei@gmail.com.

Make sure the questions.xlsx file is in the project directory.

Run the Game

```console
python game.py
```

Follow the On-Screen Instructions

Enter player names when prompted (comma-separated).
Proceed through the game by accepting or rejecting questions, answering them, and responding to random events.
game.py: The main script to run the game. 
questions.xlsx: The Excel file containing all the quiz questions.
packages/: Directory containing all the module files.
chart.py: Handles displaying the score chart using matplotlib.
excel_reader.py: Loads questions from the Excel file.
player.py: Defines the Player class for player attributes and methods.
question.py: Defines the Question class for question attributes.
sound_manager.py: Manages playing sound effects (note: works only on Windows).
timer.py: Implements the timer functionality for reading and answering phases.

## Gameplay Instructions
Starting the Game: Run game.py and enter player names when prompted.

Accepting Questions: Players are offered a question with its domain and difficulty. They can choose to accept or redraw.

Answering Questions:
- Reading Time: Players have a calculated time to read the question (not displayed).
- Answering Time: A timer is displayed while the player answers the question.
- Submitting Answers: After answering, confirm whether the answer was correct.

Random Events:
- Challenge: Players can challenge opponents. If the current player answers correctly, the opponent loses points.
- Skip Turn: Players can force an opponent to skip their next turn.

Ending the Game: The game ends when all questions have been asked or players choose not to continue after a round. A score chart is displayed at the end.

## Contributing
Contributions are welcome! Please follow these steps:

Fork the Repository

Create a New Branch
```console
git checkout -b feature/your-feature-name
```
Commit Your Changes
```console
git commit -am 'Add some feature'
```

Push to the Branch
```console
git push origin feature/your-feature-name
```

Create a Pull Request

## License
This project is licensed under the MIT License.