import streamlit as st
import logging
from youtube_utils import fetch_youtube_video_details, fetch_audio_from_youtube
from whisperx_utils import (
    convert_audio_to_transcript,
    convert_transcript_to_json_str,
    convert_transcript_to_plain_text,
)


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


def clear_url():
    st.session_state["url"] = ""


def session_state_input_url(youtube_url: str):
    logger = logging.getLogger(__name__)
    logger.info("Processing URL: %s", youtube_url)
    info = fetch_youtube_video_details(youtube_url)
    logger.info("Video info for video %s retrieved successfully.", info.get("id"))
    # logger.info("Uploader: %s", info.get("uploader"))
    # logger.info("Title: %s", info.get("title"))
    # logger.info("Duration: %s", human_readable_time(info.get("duration")))
    # logger.info("Thumbnail: %s", info.get("thumbnail"))
    # logger.info("Description: %s", info.get("description"))
    # logger.info("Language: %s", info.get("language"))
    # set_url(youtube_url)
    set_stage(1)


def session_state_extract_audio():
    logger = logging.getLogger(__name__)
    youtube_url = st.session_state.url
    extract_audio = st.button("Extract audio")
    if not extract_audio:
        return
    with st.spinner("Extracting audio..."):
        logger.info("Extracting audio from video %s", youtube_url)
        audio_filename = fetch_audio_from_youtube(youtube_url)
        logger.info("Audio extracted successfully.")
        set_filename(audio_filename)
    set_stage(2)
    st.rerun()


def session_state_transcribe_audio():
    logger = logging.getLogger(__name__)
    audio_filename = st.session_state.filename
    transcribe_audio = st.button("Transcribe audio")
    if not transcribe_audio:
        return
    with st.spinner("Transcribing audio..."):
        logger.info("Transcribing audio from file %s", audio_filename)
        transcript = convert_audio_to_transcript(audio_filename)
        if not transcript:
            logger.error("Failed to transcribe audio.")
            st.error("Failed to transcribe audio. Please try again.")
            return
        logger.info("Audio transcribed successfully.")
        set_transcript(transcript)
    set_stage(3)
    st.rerun()


def session_state_show_transcript():
    transcript = st.session_state.transcript
    st.write("Transcription complete!")
    with st.container(height=300):
        st.json(st.session_state.transcript)
    st.download_button(
        label="Download Transcript as JSON",
        data=convert_transcript_to_json_str(transcript),
        file_name="transcript.json",
        mime="application/json",
    )
    st.download_button(
        label="Download Transcript as plain text",
        data=convert_transcript_to_plain_text(transcript),
        file_name="transcript.txt",
        mime="text/plain",
    )
    session_done = st.button("Start Over", on_click=clear_url)
    if session_done:
        init_session_state(force=True)
        st.rerun()


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    init_session_state()

    st.title("TubeScribe")
    youtube_url = st.text_input("Enter a YouTube video URL", "", key="url")
    if st.session_state.stage == 0 and youtube_url:
        session_state_input_url(youtube_url)

    if st.session_state.stage == 1:
        session_state_extract_audio()

    if st.session_state.stage == 2:
        session_state_transcribe_audio()

    if st.session_state.stage == 3:
        session_state_show_transcript()


main()
