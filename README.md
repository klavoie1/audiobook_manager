 # Audiobook Player

A simple and lightweight Python-based audiobook player that remembers the last known position for any number of 
audiobooks. This player allows you to load, play, pause, and resume audiobooks, with bookmarks automatically 
saved so you can pick up right where you left off.

## Features
- Playback Controls: Play, pause, and stop functionality for audiobooks.
- Automatic Bookmarking: Saves the last known playback position for each audiobook.
- Multiple Audiobooks: Supports any number of audiobooks, each with its own saved position.
- Lightweight & Simple: Built using Python with `tkinter` for the GUI and `pydub` for audio playback.

## Libraries Used
- `tkinter`: For building the graphical user interface (GUI).
- `pydub` and `pyaudio`: For audio playback and streaming.
- `sqlite3`: For storing the last known positions of audiobooks.
- `mutagen`: For reading metadata from audio files (e.g., title, author).
- `numpy`: For fixing audio issues created from volume changes.

## Installation
1. Clone the repository:
```bash
git clone https://github.com/klavoie1/audiobook_manager.git
cd audiobook_manager
```

2. Install the required dependencies using pip:
```bash
pip install -r requirements.txt 
```
The `requirements.txt` file includes the necessary libraries (`pydub`, `pyaudio`, `mutagen`).

3. Make sure you have `ffmpeg` installed for `pydub` to work properly with MP3 files.
- For Windows, download ffmpeg <a href="https://ffmpeg.org/download.html">here</a>.
- For Linux/Mac, install it via package managers like apt, brew, etc.

## Usage
Run the program:

```bash
python main.py
```

The main window will appear. You can:
- Load an audiobook: Click the "Load Audiobook" button to choose an audio file.
- Play, Pause, or Stop: Use the provided buttons to control the playback.
- Resume where you left off: The player will automatically remember the last position of the audiobook when paused or stopped.

## File Format Support
The player supports a variety of audio file formats, including:

- `.mp3`
- `.wav`
- `.m4a`
- And other formats supported by `pydub`.

## Database
The player uses an SQLite database to store the last known playback position of each audiobook. 
This is stored in a local file `data/bookmarks.db`. Each time you pause or stop an audiobook, 
the player saves the current position, and it will resume from that position the next time the file is loaded.

## Project Structure
```graphsql
audiobook_player/
│
├── main.py                      # Entry point – launches the GUI
│ 
├── player/                      # Core playback and bookmarking logic
│   ├── audio_manager.py         # Audio playback using pydub + pyaudio
│   └── bookmark_manager.py      # Bookmark save/load using sqlite3
│ 
├── ui/                          # GUI built with tkinter
│   └── main_window.py           # Main tkinter window and controls
│ 
├── utils/                       # Utilities like file handling and metadata
│   └── file_utils.py            # Uses mutagen to read metadata
│ 
├── data/                        # Contains the SQLite database
│   └── bookmarks.db             # Stores audiobook file positions
│ 
├── requirements.txt             # List of external Python libraries
└── README.md                    # Project overview and usage
```

## Future Improvements

- Search functionality: Allow users to search for audiobooks in their library.
- Playlist support: Create playlists of multiple audiobooks and control the order. 
- Customization: Add options for customizing the UI (themes, font sizes, etc.).
- Cross-platform support: Test on multiple operating systems (Windows, macOS, Linux).

## License

This project is licensed under the MIT License - see the LICENSE file for details.
