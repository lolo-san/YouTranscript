import warnings
from matplotlib import MatplotlibDeprecationWarning

# Suppress warnings from pyannote
warnings.filterwarnings("ignore", category=MatplotlibDeprecationWarning, module="^pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="^pyannote")
warnings.filterwarnings("ignore", category=DeprecationWarning, module="^pkg_resources")

import numpy as np
import pytest
from unittest.mock import patch
from app.whisperx_utils import convert_audio_to_transcript

@pytest.mark.parametrize("dummy_audio_data", [
    np.random.randn(16000).astype(np.float32),
])
@patch("whisperx.load_audio")          # 1) Mock load_audio
@patch("whisperx.load_model")          # 2) Mock load_model
def test_convert_audio_to_transcript(mock_load_model, mock_load_audio, dummy_audio_data):
    # Mock whisperx.load_audio to return some dummy audio samples
    mock_load_audio.return_value = dummy_audio_data

    # Mock load_model to return a FakeModel with a transcribe method
    class FakeModel:
        def transcribe(self, audio, batch_size=4):
            return {"segments": [{"text": "Hello World"}], "language": "en"}

    mock_load_model.return_value = FakeModel()

    # Now call your function
    result_json = convert_audio_to_transcript("fake_audio_file.wav")

    assert result_json["segments"][0]["text"] == "Hello World"
    assert result_json["language"] == "en"
