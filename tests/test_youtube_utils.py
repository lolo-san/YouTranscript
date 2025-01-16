import warnings
from matplotlib import MatplotlibDeprecationWarning

# Suppress warnings from pyannote
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning, module="^pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="^pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="^pkg_resources")

# test_yt_utils.py
import yt_dlp
import pytest
from unittest.mock import patch, MagicMock
from requests.exceptions import HTTPError
from app.youtube_utils import fetch_youtube_metadata_and_thumbnail
from app.youtube_utils import fetch_youtube_audio_track


@pytest.fixture
def fake_info_dict():
    """A fake info dict that yt_dlp might return on success."""
    return {
        "id": "abc123",
        "uploader": "CoolUploader",
        "title": "Sample Video Title",
        "duration": 360,
        "description": "This is a sample description",
        "language": "en",
        # plus any other keys that yt_dlp might include
    }

def test_fetch_youtube_metadata_and_thumbnail_success(fake_info_dict, tmp_path):
    """
    Test a successful retrieval of metadata and thumbnail.
    We mock yt_dlp so we don't hit the network.
    """
    # 1) Create a mock that returns fake_info_dict
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=fake_info_dict):
        # 2) Call your function
        url = "https://youtube.com/watch?v=abc123"
        result = fetch_youtube_metadata_and_thumbnail(url)

    # 3) Verify we get the subset_info in return
    assert result["id"] == fake_info_dict["id"]
    assert result["uploader"] == fake_info_dict["uploader"]
    assert result["title"] == fake_info_dict["title"]
    assert result["duration"] == fake_info_dict["duration"]
    assert result["description"] == fake_info_dict["description"]
    assert result["language"] == fake_info_dict["language"]

def test_fetch_youtube_audio_track_success(tmp_path):
    """
    Test a successful retrieval of audio track.
    We mock yt_dlp so we don't hit the network.
    """
    # 1) Create a mock that returns the audio filepath
    with patch.object(yt_dlp.YoutubeDL, 'extract_info', return_value=fake_info_dict):
        with patch.object(yt_dlp.YoutubeDL, 'prepare_filename', return_value="/path/to/audio.mp3"):
            # 2) Call your function
            url = "https://youtube.com/watch?v=abc123"
            result = fetch_youtube_audio_track(url)
            
    # 3) Verify we get the audio filepath in return
    assert result == "/path/to/audio.mp3"
