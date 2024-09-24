# timer.py

import threading
import time


class Timer:
    def __init__(self, root, duration, callback):
        """
        Initialize a Timer object.

        Args:
            root (tk.Tk): The main Tkinter window or a widget.
            duration (float): The duration of the timer in seconds.
            callback (function): The function to call when the timer expires.
        """
        self.root = root
        self.duration = duration
        self.callback = callback
        self.thread = None
        self.start_time = None
        self.time_remaining = duration
        self.is_running = False

    def start(self):
        """
        Start the timer.
        """
        self.is_running = True
        self.start_time = time.time()
        self.thread = threading.Thread(target=self.run)
        self.thread.start()

    def run(self):
        """
        Run the timer in a separate thread.
        """
        while self.is_running and self.time_remaining > 0:
            time.sleep(0.1)
            elapsed_time = time.time() - self.start_time
            self.time_remaining = self.duration - elapsed_time
            # Update the GUI timer display
            self.root.after(0, self.update_display)
        if self.is_running:
            self.is_running = False
            # Timer expired; call the callback function
            self.root.after(0, self.callback)

    def update_display(self):
        """
        Update the timer display in the GUI.
        """
        minutes = int(self.time_remaining) // 60
        seconds = int(self.time_remaining) % 60
        time_str = f"Time Remaining: {minutes:02d}:{seconds:02d}"
        # Assuming there's a label in the root window to display the timer
        if hasattr(self.root, "timer_label"):
            self.root.timer_label.configure(text=time_str)

    def cancel(self):
        """
        Cancel the timer.
        """
        self.is_running = False
        self.time_remaining = 0
        # Do not join the thread here
        # if self.thread is not None:
        #     self.thread.join()
        # Clear the timer display
        self.root.after(0, self.clear_display)

    def clear_display(self):
        """
        Clear the timer display in the GUI.
        """
        if hasattr(self.root, "timer_label"):
            self.root.timer_label.configure(text="")
