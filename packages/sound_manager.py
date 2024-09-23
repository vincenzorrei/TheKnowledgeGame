# sound_manager.py

import os
import platform
import threading

if platform.system() == "Windows":
    import winsound
else:
    # For non-Windows systems, we can use the simpleaudio module
    try:
        import simpleaudio as sa
    except ImportError:
        print(
            "simpleaudio module not found. Please install it using 'pip install simpleaudio'."
        )


class SoundManager:
    def __init__(self):
        """
        Initialize the SoundManager.
        """
        # Define paths to your sound files
        self.correct_sound_path = os.path.join("sounds", "correct.wav")
        self.incorrect_sound_path = os.path.join("sounds", "incorrect.wav")
        self.time_up_sound_path = os.path.join("sounds", "time_up.wav")
        self.challenge_sound_path = os.path.join("sounds", "challenge.wav")
        self.skip_sound_path = os.path.join("sounds", "skip.wav")

    def play_sound(self, sound_path):
        """
        Play a sound from the given file path in a separate thread.
        """
        threading.Thread(target=self._play_sound_thread, args=(sound_path,)).start()

    def _play_sound_thread(self, sound_path):
        """
        Play sound in a separate thread to avoid blocking the main thread.
        """
        if platform.system() == "Windows":
            winsound.PlaySound(sound_path, winsound.SND_FILENAME | winsound.SND_ASYNC)
        else:
            try:
                wave_obj = sa.WaveObject.from_wave_file(sound_path)
                play_obj = wave_obj.play()
                play_obj.wait_done()
            except Exception as e:
                print(f"Error playing sound: {e}")

    def play_correct_sound(self):
        """
        Play the sound for a correct answer.
        """
        self.play_sound(self.correct_sound_path)

    def play_incorrect_sound(self):
        """
        Play the sound for an incorrect answer.
        """
        self.play_sound(self.incorrect_sound_path)

    def play_time_up_sound(self):
        """
        Play the sound when time is up.
        """
        self.play_sound(self.time_up_sound_path)

    def play_challenge_sound(self):
        """
        Play the sound for a challenge event.
        """
        self.play_sound(self.challenge_sound_path)

    def play_skip_sound(self):
        """
        Play the sound for a skip turn event.
        """
        self.play_sound(self.skip_sound_path)
