from mutagen import File
import os

def get_metadata(file_path):
    """
    Extract metadata from an audio file using mutagen.
    Returns a dictionary with basic information.
    """
    metadata = {}

    try:
        audio = File(file_path, easy=True)

        if audio is None:
            return metadata

        metadata['title'] = audio.get('title', [None])[0]
        metadata['artist'] = audio.get('artist', [None])[0]
        metadata['album'] = audio.get('album', [None])[0]
        metadata['duration'] = audio.info.length if audio.info else None

    except Exception as e:
        print(f"Error reading metadata from {file_path}: {e}")

    return metadata


def get_audio_format(file_path):
    """
    Returns the format of the audio file based on the extension.
    Useful for pydub loading.
    """
    extension = file_path.split('.')[-1].lower()
    if extension in ['mp3', 'wav', 'm4a', 'm4b', 'flac', 'ogg']:
        return extension
    else:
        return 'mp3'  # Default fallback



def get_title(file_path):
    """Gets the title of the audio file based on the extension."""
    try:
        audio = File(file_path, easy=True)

        if audio is None:
            return os.path.basename(file_path)

        title = audio.get('title', [None])[0]
        return title if title else os.path.basename(file_path)

    except Exception as e:
        print(f"Error reading title from {file_path}: {e}")
        return os.path.basename(file_path)