# File used to manage audio with pyaudio and pydub

from pydub import AudioSegment
from pydub.playback import play
import simpleaudio


class AudioManager:
    def __init__(self):
        self.audio = None  # Loaded AudioSegment
        self.play_obj = None  # simpleaudio.PlayObject
        self.paused = False
        self.pause_position = 0  # In milliseconds

    def load(self, file_path):
        """Load an audio file that will be played."""
        try:
            self.audio = AudioSegment.from_file(file_path)
            self.play_obj = None
            self.paused = False
            self.pause_position = 0
            print(f"Loaded audio: {file_path}")
        except Exception as e:
            print(f"Error loading audio: {e}")

    def play(self):
        """Play the loaded audio"""
        if self.audio is None:
            print("No audio loaded.")
            return

        if self.paused:
            # If paused, resume from where it left off
            segment = self.audio[self.pause_position:]
            self.play_obj = play(segment)
            self.paused = False
            print("Resumed audio.")
        else:
            # Start fresh
            self.play_obj = play(self.audio)
            print("Started audio playback.")

    def pause(self):
        """Pause playback"""
        if self.play_obj and self.play_obj.is_playing():
            self.pause_position += int(self.play_obj.get_playback_position() * 1000 / self.play_obj.sample_rate)
            self.play_obj.stop()
            self.paused = True
            print(f"Paused at {self.pause_position} ms.")

    def stop(self):
        """Stop playback completely"""
        if self.play_obj:
            self.play_obj.stop()
            self.play_obj = None
            self.paused = False
            self.pause_position = 0
            print("Stopped audio.")
