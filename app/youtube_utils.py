import yt_dlp
import logging
from urllib.error import HTTPError
from pathlib import Path

TMP_DIR = Path("./tmp")
TMP_DIR.mkdir(exist_ok=True)


def fetch_youtube_metadata_and_thumbnail(url: str) -> dict:
    """
    Fetch metadata and thumbnail from YouTube URL.
    Returns the final info dict from yt_dlp, which includes
    metadata about where files are saved
    """
    ydl_opts = {
        "skip_download": True,
        "outtmpl": f"{TMP_DIR}/%(id)s/%(id)s.%(ext)s",
        "writethumbnail": True,
        "no_warnings": True,
        "quiet": True,
        "writeinfojson": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
            keys_of_interest = [
                "id",
                "uploader",
                "title",
                "duration",
                "description",
                "language",
            ]
            subset_info = {key: info_dict.get(key) for key in keys_of_interest}
            subset_info["thumbnail"] = (
                f"{TMP_DIR}/{info_dict['id']}/{info_dict['id']}.webp"
            )
        return subset_info
    except HTTPError as e:
        logging.error("Failed to fetch metadata/thumbnail: %s", e)
        return {}


def fetch_youtube_audio_track(url: str) -> str:
    """
    Download audio track from YouTube URL.
    Returns the filepath of the downloaded
    audio file.
    """
    ydl_opts = {
        "format": "bestaudio/best",
        "outtmpl": f"{TMP_DIR}/%(id)s/%(id)s.%(ext)s",
        "no_warnings": True,
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info_dict = ydl.extract_info(url, download=True)
        return ydl.prepare_filename(info_dict)
    except HTTPError as e:
        logging.error("Failed to fetch audio: %s", e)
        return ""
