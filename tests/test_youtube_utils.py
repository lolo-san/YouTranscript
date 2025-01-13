import warnings
from matplotlib import MatplotlibDeprecationWarning

# Suppress warnings from pyannote
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning, module="^pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="^pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="^pkg_resources")

import yt_dlp
from unittest.mock import patch
from app.youtube_utils import fetch_youtube_video_details
from app.youtube_utils import fetch_audio_from_youtube

def test_get_video_info_success():
    fake_info = {"id": "abc123", "title": "Test Video", "duration": 120}

    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=fake_info):
        info = fetch_youtube_video_details("https://fake_url")
        assert info["id"] == "abc123"
        assert info["title"] == "Test Video"
        assert info["duration"] == 120

def test_get_video_info_failure():
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', side_effect=Exception("Failed to fetch")):
        info = fetch_youtube_video_details("https://fake_url")
        assert info == {}

def test_fetch_audio_success(tmp_path):
    fake_info = {"id": "abc123", "title": "Test Video", "duration": 120, "ext": "webm"}

    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=fake_info):
        with patch.object(yt_dlp.YoutubeDL, 'prepare_filename', return_value=str(tmp_path / "abc123.webm")):
            audio_file = fetch_audio_from_youtube("https://fake_url", output_path=str(tmp_path))
            assert audio_file.endswith("abc123.webm")

def test_fetch_audio_failure(tmp_path):
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', side_effect=Exception("Failed to fetch")):
        audio_file = fetch_audio_from_youtube("https://fake_url", output_path=str(tmp_path))
        assert audio_file == ""