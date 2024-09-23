# excel_reader.py

import pandas as pd

from packages.question import Question


class ExcelReader:
    def __init__(self, file_path):
        """
        Initialize the ExcelReader with the path to the Excel file.

        Args:
            file_path (str): The path to the Excel file containing the questions.
        """
        self.file_path = file_path

    def load_questions(self):
        """
        Load questions from the Excel file and return a list of Question objects.

        Returns:
            List[Question]: A list of Question instances.
        """
        try:
            # Read the Excel file into a DataFrame
            df = pd.read_excel(self.file_path)

            # Ensure required columns are present
            required_columns = ["Question", "Domain", "Difficulty"]
            if not all(column in df.columns for column in required_columns):
                raise ValueError(
                    f"The Excel file must contain the columns: {', '.join(required_columns)}"
                )

            # Create Question objects
            questions = []
            for _, row in df.iterrows():
                text = str(row["Question"]).strip()
                domain = str(row["Domain"]).strip()
                difficulty = int(row["Difficulty"])

                question = Question(text=text, domain=domain, difficulty=difficulty)
                questions.append(question)

            return questions

        except FileNotFoundError:
            print(f"Error: The file {self.file_path} was not found.")
            return []
        except Exception as e:
            print(f"An error occurred while reading the Excel file: {e}")
            return []
