import tkinter as tk
from tkinter import ttk, filedialog
from player.audio_manager import AudioManager
from utils.file_utils import get_title

class MainWindow(tk.Tk):
    def __init__(self):
        # Main setup for GUI window
        super().__init__()
        self.title('Audiobook Player')
        self.geometry('800x600')

        # Calling the widget class for the UI elements
        self.menu = Menu(self)

        # Running command for the main window
        self.mainloop()


class Menu(ttk.Frame):
    """This Class is where a majority of the elements for the audio player will be created and later called in the main class."""
    def __init__(self, parent):
        super().__init__(parent)

        self.audio_manager = AudioManager()
        self.file_label = None
        self.current_file = None
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('TitleLabel.TLabel',
                        foreground='black',     # Text color
                        font=('Verdana', 32, 'bold'))

        ttk.Label(self, text="Audiobook Player", style="TitleLabel.TLabel").grid(column=0, row=0)

        ttk.Button(self, text="Load Audio", command=self.load_audio).grid(column=0, row=1)

        # Initialize file_label here
        self.file_label = ttk.Label(self, text="No file loaded", style="TitleLabel.TLabel")
        self.file_label.grid(column=0, row=2)

        self.pack(expand=False, fill="both")

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audiobook Files", "*.m4b *.mp3 *.wav *.m4a *.flac")])
        if file_path:
            self.current_file = file_path
            title = get_title(file_path)  # This will get the title from the file
            self.file_label.config(text=title)  # Update the file label with the title
            self.audio_manager.load(file_path)

    def play_audio(self):
        self.audio_manager.play()

    def pause_audio(self):
        self.audio_manager.pause()

    def stop_audio(self):
        self.audio_manager.stop()


class MediaSlider(ttk.Frame):
    """This class is a sub Frame for the media slider"""
    def __init__(self, parent):
        super().__init__(parent)


class MediaControls(ttk.Frame):
    """This class is a sub Frame for the media controls"""
    def __init__(self, parent):
        super().__init__(parent)
