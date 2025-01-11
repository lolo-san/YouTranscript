import streamlit as st
import yt_dlp
import whisperx
import logging
import json

AUDIO_CACHE_DIR = "./tmp/audio"


def get_video_info(url: str) -> dict:
    """
    Get video information from YouTube URL.

    :param url: YouTube video URL
    :return: Video information dictionary
    """
    ydl_opts = {
        "quiet": True,
        "no_warnings": True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return info_dict


def human_readable_time(seconds: int) -> str:
    """
    Convert seconds to a human-readable format (HH:MM:SS).

    :param seconds: Time in seconds
    :return: Human-readable time string
    """
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"


def fetch_audio_from_youtube(url: str, output_path=AUDIO_CACHE_DIR) -> str:
    """
    Download audio from YouTube URL.

    :param url: YouTube video URL
    :param output_path: Path to save the downloaded audio file
    :return: Path to the downloaded audio file
    """
    ydl_opts = {
        "format": "bestaudio/best",  # highest quality audio
        "outtmpl": f"{output_path}/%(id)s.%(ext)s",
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info and download the file
        info_dict = ydl.extract_info(url, download=True)
        # Get the actual local file name
        filepath = ydl.prepare_filename(info_dict)
    return filepath


def convert_audio_to_transcript(audio_file: str) -> json:
    """
    Transcribe audio using WhisperX.

    :param audio_file: Path to the audio file
    :return: Transcription result
    """
    device = "cuda"
    batch_size = 4  # reduce if low on GPU mem
    compute_type = "float16"  # change to "int8" if low on GPU mem (may reduce accuracy)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    return json.dumps(result, indent=2, ensure_ascii=False)


def convert_transcript_to_plain_text(transcript: json) -> str:
    """
    Convert WhisperX transcript to plain text.

    :param transcript: WhisperX transcript JSON
    :return: Plain text transcript
    """
    transcript = json.loads(transcript)
    return "\n".join([seg["text"] for seg in transcript["segments"]])


def set_stage(i):
    st.session_state.stage = i


def set_filename(s):
    st.session_state.filename = s


def set_transcript(s):
    st.session_state.transcript = s


def init_session_state(force=False):
    if "stage" not in st.session_state or force:
        st.session_state.stage = 0

    if "filename" not in st.session_state or force:
        st.session_state.filename = ""

    if "transcript" not in st.session_state or force:
        st.session_state.transcript = ""


def main():

    # Configure the logging
    logging.basicConfig(
        level=logging.INFO,  # Set to DEBUG for more verbose output
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[
            logging.StreamHandler()  # You can add FileHandler here to log to a file
        ],
    )
    logger = logging.getLogger(__name__)

    # Initialize the session state
    init_session_state()

    st.title("TubeScribe")
    youtube_url = st.text_input("Enter a YouTube video URL")
    if st.session_state.stage == 0 and youtube_url:
        logger.info("Processing URL: %s", youtube_url)
        try:
            info = get_video_info(youtube_url)
            logger.info(
                "Video info for video %s retrieved successfully.", info.get("id")
            )
            logger.info("Uploader: %s", info.get("uploader"))
            logger.info("Title: %s", info.get("title"))
            logger.info("Duration: %s", human_readable_time(info.get("duration")))
            logger.info("Thumbnail: %s", info.get("thumbnail"))
            logger.info("Description: %s", info.get("description"))
            logger.info("Language: %s", info.get("language"))
        except Exception as e:
            logger.error("Error retrieving video info: %s", e)
            st.error(f"Failed to retrieve video info: {e}")
        set_stage(1)

    if st.session_state.stage == 1:
        extract_audio = st.button("Extract Audio")
        if extract_audio:
            with st.spinner("Extracting audio..."):
                logger.info("Extracting audio from video %s", youtube_url)
                audio_filename = fetch_audio_from_youtube(youtube_url)
                logger.info("Audio extracted successfully.")
                set_filename(audio_filename)
            set_stage(2)
            st.rerun()

    if st.session_state.stage == 2:
        transcribe_audio = st.button("Transcribe Audio")
        if transcribe_audio:
            with st.spinner("Transcribing audio..."):
                audio_filename = st.session_state.filename
                logger.info("Transcribing audio from file %s", audio_filename)
                transcript = convert_audio_to_transcript(audio_filename)
                logger.info("Audio transcribed successfully.")
                set_transcript(transcript)
            set_stage(3)
            st.rerun()

    if st.session_state.stage == 3:
        st.write("Transcription complete!")
        with st.container(height=300):
            st.json(st.session_state.transcript)
        st.download_button(
            label="Download Transcript as JSON",
            data=st.session_state.transcript,
            file_name="transcript.json",
            mime="application/json",
        )
        st.download_button(
            label="Download Transcript as plain text",
            data=convert_transcript_to_plain_text(st.session_state.transcript),
            file_name="transcript.txt",
            mime="application/json",
        )
        session_done = st.button("Start Over")
        if session_done:
            init_session_state(force=True)
            st.rerun()


main()
