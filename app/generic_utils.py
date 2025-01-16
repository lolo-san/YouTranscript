from enum import Enum, auto


class Stage(Enum):
    ENTER_URL = auto()
    EXTRACT_AUDIO = auto()
    TRANSCRIBE_AUDIO = auto()
    SHOW_TRANSCRIPT = auto()


def human_readable_time(seconds: int) -> str:
    """
    Convert seconds to a human-readable format (HH:MM:SS).

    :param seconds: Time in seconds
    :return: Human-readable time string
    :rtype: str
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"
