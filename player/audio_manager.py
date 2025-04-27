from pydub import AudioSegment
from pyaudio import PyAudio, paInt16
import threading
import time
import numpy as np


class AudioManager:
    def __init__(self):
        self.position_ms = 0
        self.audio = None
        self.position = 0  # Position in seconds
        self.playing = False
        self.stream = None
        self.audio_thread = None
        self.pyaudio = PyAudio()
        self.file_path = None
        self._stop_event = threading.Event()
        self.volume = 1.0  # Default volume (1.0 means no change)

    def load(self, file_path, start_position=0.0):
        """Loads an audiobook and optionally starts at a specified position (in seconds)."""
        self.audio = AudioSegment.from_file(file_path)
        self.file_path = file_path
        self.position = start_position
        self.position_ms = int(self.position * 1000)

        if self.stream:
            self.stream.close()

        self.stream = self.pyaudio.open(format=self.pyaudio.get_format_from_width(self.audio.sample_width),
                                        channels=self.audio.channels,
                                        rate=self.audio.frame_rate,
                                        output=True)

    def _apply_volume(self, audio_segment):
        """Applies the volume change by scaling the audio samples."""
        # Convert audio segment to numpy array of samples
        samples = np.array(audio_segment.get_array_of_samples(), dtype=np.int16)

        # Apply volume scaling (clip values to avoid overflow)
        samples = np.clip(samples * self.volume, -32768, 32767).astype(np.int16)

        # Create a new audio segment with adjusted volume
        return audio_segment._spawn(samples.tobytes())

    def _play_audio(self):
        """Internal method to play audio from current position in a separate thread."""
        segment = self.audio[self.position_ms:]
        chunk_length = 50  # milliseconds per chunk

        self.playing = True
        for chunk_start in range(0, len(segment), chunk_length):
            if not self.playing or self._stop_event.is_set():
                break  # If paused/stopped

            chunk = segment[chunk_start:chunk_start + chunk_length]

            # Apply volume change to the audio chunk
            chunk = self._apply_volume(chunk)

            # Convert to raw data and play
            self.stream.write(chunk.raw_data)

            self.position_ms += chunk_length
            self.position = self.position_ms / 1000

        self.playing = False

    def play(self):
        """Starts playing audio without blocking the GUI."""
        if not self.audio:
            print("No audio loaded.")
            return

        if self.audio_thread and self.audio_thread.is_alive():
            print("Already playing.")
            return

        self._stop_event.clear()
        self.audio_thread = threading.Thread(target=self._play_audio)
        self.audio_thread.start()

    def pause(self):
        """Pauses playback."""
        self.playing = False

    def stop(self):
        """Stops playback and resets position."""
        self.playing = False
        self.position = 0
        self.position_ms = 0
        self._stop_event.set()

    def get_position(self):
        """Returns the current position in seconds."""
        return self.position

    def close(self):
        """Cleans up resources when done."""
        self.playing = False
        self._stop_event.set()
        if self.stream:
            self.stream.stop_stream()
            self.stream.close()
        self.pyaudio.terminate()

    def get_audio_length(self):
        """Returns total length of the loaded audio (in seconds)."""
        return len(self.audio) / 1000 if self.audio else 0

    def seek(self, new_position):
        """Seeks to a new position in the audio (in seconds)."""
        self.pause()  # Pause first
        self._stop_event.set()  # Stop any existing audio thread
        if self.audio_thread and self.audio_thread.is_alive():
            self.audio_thread.join()  # Wait until thread actually stops

        self._stop_event.clear()
        self.position = new_position
        self.position_ms = int(new_position * 1000)
        self.play()  # Restart playing from new position

    def set_volume(self, volume):
        """Sets the volume, where volume is a float value between 0.0 and 1.0"""
        self.volume = volume
        print(f"Volume set to: {self.volume}")
