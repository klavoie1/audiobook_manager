import tkinter as tk
from tkinter import ttk, filedialog
from player.audio_manager import AudioManager
from player.bookmark_manager import BookmarkManager
from utils.file_utils import get_title


class MainWindow(tk.Tk):
    def __init__(self):
        # Main setup for GUI window
        super().__init__()
        self.title('Audiobook Player')
        self.geometry('800x600')

        # Calling the widget class for the UI elements
        self.main = Main(self)


        # Running command for the main window
        self.mainloop()


class Main(ttk.Frame):
    def __init__(self, parent):
        super().__init__(parent)

        from player.bookmark_manager import BookmarkManager
        self.audio_manager = AudioManager()
        self.bookmark_manager = BookmarkManager()

        self.current_file = None
        self.audio_length = 0
        self.user_seeking = False

        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        style = ttk.Style()
        style.configure('TitleLabel.TLabel', foreground='black', font=('Verdana', 32, 'bold'))

        ttk.Label(self, text="Audiobook Player", style="TitleLabel.TLabel").grid(column=0, row=0, columnspan=3)

        ttk.Button(self, text="Load Audio", command=self.load_audio).grid(column=0, row=2)

        ttk.Button(self, text="Play", command=self.play_audio).grid(column=2, row=2)
        ttk.Button(self, text="Pause", command=self.pause_audio).grid(column=3, row=2)
        ttk.Button(self, text="Stop", command=self.stop_audio).grid(column=4, row=2)

        # Volume Control Slider
        self.volume_slider = ttk.Scale(self, from_=0.0, to=1.0, orient="horizontal", command=self.adjust_volume)
        self.volume_slider.set(1.0)  # Default volume is 1.0 (full volume)
        self.volume_slider.grid(column=0, row=1)

        # Slider for seeking
        self.seek_slider = ttk.Scale(self, from_=0, to=100, orient='horizontal')
        self.seek_slider.grid(column=0, row=3, columnspan=3, sticky="ew", pady=10)

        # Bind mouse events for smoother seeking
        self.seek_slider.bind("<Button-1>", self.start_seeking)
        self.seek_slider.bind("<ButtonRelease-1>", self.end_seeking)

        # Label for showing time
        self.time_label = ttk.Label(self, text="00:00:00 / 00:00:00")
        self.time_label.grid(column=0, row=4, columnspan=3, pady=5)

        self.file_label = ttk.Label(self, text="No file loaded")
        self.file_label.grid(column=0, row=5, columnspan=3)

        self.pack(expand=True, fill="both")

        menu = tk.Menu(parent)
        file_menu = tk.Menu(menu, tearoff=False)
        file_menu.add_command(label="Open", command=self.load_audio)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)
        menu.add_cascade(label="File", menu=file_menu)
        parent.configure(menu=menu)

        parent.protocol("WM_DELETE_WINDOW", self.on_exit)

        self.update_slider()

    def load_audio(self):
        file_path = filedialog.askopenfilename(filetypes=[("Audiobook Files", "*.m4b *.mp3 *.wav *.m4a *.flac")])
        if file_path:
            self.current_file = file_path
            title = get_title(file_path)
            self.file_label.config(text=title)

            last_position = self.bookmark_manager.get_bookmark(file_path)
            self.audio_manager.load(file_path, start_position=last_position)

            self.audio_length = self.audio_manager.get_audio_length()
            self.seek_slider.config(to=self.audio_length)

    def play_audio(self):
        self.audio_manager.play()

    def pause_audio(self):
        self.audio_manager.pause()
        if self.current_file:
            position = self.audio_manager.get_position()
            self.bookmark_manager.save_bookmark(self.current_file, position)

    def stop_audio(self):
        self.audio_manager.stop()
        if self.current_file:
            self.bookmark_manager.save_bookmark(self.current_file, 0.0)
        self.seek_slider.set(0)

    def start_seeking(self, event):
        """User starts dragging the slider."""
        self.user_seeking = True

    def end_seeking(self, event):
        """User releases the slider."""
        self.user_seeking = False
        value = self.seek_slider.get()
        self.seek(value)

    def seek(self, value):
        """Jump to the selected position."""
        if self.audio_manager.audio:
            new_position = float(value)
            self.audio_manager.seek(new_position)

    def update_slider(self):
        """Update the slider and time label every 500ms."""
        if not self.user_seeking and self.audio_manager.playing and self.audio_manager.audio:
            current_pos = self.audio_manager.get_position()
            self.seek_slider.set(current_pos)

        # Update time display
        current = self.audio_manager.get_position()
        total = self.audio_length
        self.time_label.config(text=f"{self.format_time(current)} / {self.format_time(total)}")

        self.after(500, self.update_slider)

    def adjust_volume(self, val):
        """Adjusts the volume based on the slider value."""
        volume = float(val)
        self.audio_manager.set_volume(volume)

    @staticmethod
    def format_time(seconds):
        """Formats seconds into hh:mm:ss."""
        h = int(seconds) // 3600
        m = (int(seconds) % 3600) // 60
        s = int(seconds) % 60
        return f"{h:02}:{m:02}:{s:02}"

    def on_exit(self):
        self.pause_audio()
        self.audio_manager.close()
        self.master.destroy()

