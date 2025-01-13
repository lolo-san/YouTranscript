import logging
import yt_dlp

AUDIO_CACHE_DIR = "./tmp/audio"


def fetch_youtube_video_details(url: str) -> dict:
    """
    Fetch video informations from the YouTube URL.

    :param url: YouTube video URL
    :return: Video information dictionary
    :rtype: dict
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=False)
        return info_dict
    except Exception as e:
        logging.error("Failed to fetch video details: %s", e)
        return {}


def fetch_audio_from_youtube(url: str, output_path=AUDIO_CACHE_DIR) -> str:
    """
    Download audio from YouTube URL.

    :param url: YouTube video URL
    :param output_path: Path to save the downloaded audio file
    :return: Path to the downloaded audio file
    :rtype: str
    """
    ydl_opts = {
        "format": "bestaudio/best",  # highest quality audio
        "outtmpl": f"{output_path}/%(id)s.%(ext)s",
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            # Extract info and download the file
            info_dict = ydl.extract_info(url, download=True)
            # Get the actual local file name
            filepath = ydl.prepare_filename(info_dict)
        return filepath
    except Exception as e:
        logging.error("Failed to fetch audio: %s", e)
        return ""
