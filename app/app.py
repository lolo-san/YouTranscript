import streamlit as st
import logging
from pathlib import Path
from generic_utils import Stage, human_readable_time
from youtube_utils import (
    fetch_youtube_metadata_and_thumbnail,
    fetch_youtube_audio_track,
)
from whisperx_utils import (
    convert_audio_to_transcript,
    convert_transcript_to_json_str,
    convert_transcript_to_plain_text,
)


def set_session_stage(new_stage: Stage):
    st.session_state.stage = new_stage


def set_session_info(d: dict):
    st.session_state.info = d


def get_session_info() -> dict:
    return st.session_state.info


def init_session_state():
    if "stage" not in st.session_state:
        st.session_state.stage = Stage.SUBMIT_VIDEO_URL
    if "info" not in st.session_state:
        st.session_state.info = {}
    if "url" not in st.session_state:
        st.session_state.url = ""


def clear_url():
    st.session_state["url"] = ""


def process_url():
    info = fetch_youtube_metadata_and_thumbnail(st.session_state.url)
    if not info:
        return
    set_session_info(info)
    set_session_stage(Stage.SUBMIT_MODEL_PARAMS)


def session_state_input_url():
    url = st.text_input(
        "Enter a YouTube video URL", "", key="url", on_change=process_url
    )
    if url:
        st.rerun()


def show_video_details(info: dict):
    st.subheader(info.get("title"))
    st.image(info.get("thumbnail"), width=720)
    duration = human_readable_time(info.get("duration"))
    language = info.get("language")
    uploader = info.get("uploader")
    st.write(f"URL: {info.get('url')}")
    st.write(f"Duration: {duration} | Language: {language} | Uploader: {uploader}")
    with st.expander("See description"):
        st.write(info.get("description"))


def show_whisperx_settings():
    left, middle, right = st.columns(3, vertical_alignment="bottom")
    device = left.selectbox("Device", options=["cuda", "cpu"])
    batch_size = middle.selectbox("Batch size", options=["1", "4", "8", "16"], index=1)
    compute_type = right.selectbox(
        "Compute type", options=["int8", "float16", "float32"], index=1
    )
    return device, batch_size, compute_type


def session_state_input_params():
    info = get_session_info()
    show_video_details(info)
    device, batch_size, compute_type = show_whisperx_settings()
    transcribe_audio = st.button("Transcribe audio")
    if not transcribe_audio:
        return
    info["device"] = device
    info["batch_size"] = int(batch_size)
    info["compute_type"] = compute_type
    set_session_stage(Stage.TRANSCRIBE_AUDIO)
    st.rerun()


def extract_audio_track(url: str) -> str:
    with st.spinner("Extracting audio..."):
        audio_filename = fetch_youtube_audio_track(url)
        if not audio_filename:
            st.error("Failed to extract audio. Please try again.")
            return ""
        return audio_filename


def transcribe_audio_track(
    audio_filename: str, language: str, device: str, batch_size: int, compute_type: str
) -> dict:
    with st.spinner("Transcribing audio..."):
        transcript = convert_audio_to_transcript(
            audio_filename, language, device, batch_size, compute_type
        )
        if not transcript:
            st.error("Failed to transcribe audio. Please try again.")
            return {}
        return transcript


def delete_audio_track(audio_filename: str):
    file_path = Path(audio_filename)
    if file_path.exists():
        file_path.unlink()


def session_state_transcribe_audio():
    info = get_session_info()
    show_video_details(info)
    url, language, device, batch_size, compute_type = (
        info.get(key)
        for key in ("url", "language", "device", "batch_size", "compute_type")
    )
    file_path = extract_audio_track(url)
    info["transcript"] = transcribe_audio_track(
        file_path, language, device, batch_size, compute_type
    )
    delete_audio_track(file_path)
    set_session_stage(Stage.VIEW_TRANSCRIPT)
    st.rerun()


def session_state_show_transcript():
    info = get_session_info()
    transcript = info["transcript"]
    st.write("Transcription complete!")
    with st.expander("See raw transcript"):
        with st.container(height=500):
            st.json(transcript)
    dl_format = st.radio("Choose a download format:", ["Plain text", "JSON"])
    if dl_format == "JSON":
        st.download_button(
            label="Download Transcript",
            data=convert_transcript_to_json_str(transcript),
            file_name=f"{info.get('title')}.json",
            mime="application/json",
        )
    else:
        header = f" This is a transcription of the video {info.get('title')} uploaded by {info.get('uploader')}\n"
        st.download_button(
            label="Download Transcript",
            data=convert_transcript_to_plain_text(transcript, header),
            file_name=f"{info.get('title')}.txt",
            mime="text/plain",
        )
    session_done = st.button("Done", on_click=clear_url)
    if session_done:
        set_session_stage(Stage.SUBMIT_VIDEO_URL)
        set_session_info({})
        st.rerun()


def main():

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.StreamHandler()],
    )

    init_session_state()

    st.title("TubeScribe")
    st.write("Welcome to TubeScribe! This app transcribes audio from YouTube videos.")

    if st.session_state.stage == Stage.SUBMIT_VIDEO_URL:
        session_state_input_url()
    elif st.session_state.stage == Stage.SUBMIT_MODEL_PARAMS:
        session_state_input_params()
    elif st.session_state.stage == Stage.TRANSCRIBE_AUDIO:
        session_state_transcribe_audio()
    elif st.session_state.stage == Stage.VIEW_TRANSCRIPT:
        session_state_show_transcript()


main()
