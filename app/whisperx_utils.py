import json
import logging
import whisperx


def convert_audio_to_transcript(
    audio_file: str, device: str, batch_size: int, compute_type: str
) -> json:
    """
    Transcribe audio using WhisperX.

    :param audio_file: Path to the audio file
    :param device: Device to use for transcription
    :param batch_size: Batch size for transcription
    :param compute_type: Compute type for transcription
    :return: Transcription result
    :rtype: json
    """
    logger = logging.getLogger(__name__)
    try:
        logger.info("Transcribing audio from file %s", audio_file)
        model = whisperx.load_model("large-v2", device, compute_type=compute_type)
        audio = whisperx.load_audio(audio_file)
        result = model.transcribe(audio, batch_size=batch_size)
        logger.info("Audio transcribed successfully.")
        return result
    except RuntimeError as e:
        logger.error("Failed to transcribe audio: %s", e)
        return {}


def convert_transcript_to_json_str(transcript: json) -> str:
    """
    Convert WhisperX transcript to JSON string.

    :param transcript: WhisperX transcript JSON
    :return: JSON string transcript
    :rtype: str
    """
    return json.dumps(transcript, indent=2, ensure_ascii=False)


def convert_transcript_to_plain_text(transcript: json, header: str) -> str:
    """
    Convert WhisperX transcript to plain text.

    :param transcript: WhisperX transcript JSON
    :return: Plain text transcript
    :rtype: str
    """
    return header + "\n".join([seg["text"] for seg in transcript["segments"]])
