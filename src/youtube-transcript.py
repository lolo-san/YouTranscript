# Workaround for PyTorch 2.6+ compatibility with pyannote/whisperx
# PyTorch 2.6 changed weights_only default to True, breaking older model checkpoints.
# This env var forces weights_only=False for all torch.load calls that don't explicitly set it.
import os

os.environ["TORCH_FORCE_NO_WEIGHTS_ONLY_LOAD"] = "1"

# Silence deprecation/user warnings from third-party libraries (torchaudio, etc.)
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=DeprecationWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# Silence verbose third-party loggers before they're imported
import logging

# Set speechbrain to WARNING level and prevent propagation
for name in [
    "speechbrain",
    "speechbrain.utils",
    "speechbrain.utils.checkpoints",
    "speechbrain.utils.quirks",
    "whisperx",
    "whisperx.asr",
    "whisperx.vads",
    "whisperx.vads.pyannote",
    "pyannote",
    "pyannote.audio",
    "pytorch_lightning",
    "pytorch_lightning.utilities",
]:
    log = logging.getLogger(name)
    log.setLevel(logging.WARNING)
    log.propagate = False

from app.app import main

main()
