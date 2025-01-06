import streamlit as st
import yt_dlp
import whisperx

AUDIO_CACHE_DIR = "./tmp/audio"
MODEL_CACHE_DIR = "./tmp/model"

def get_video_info(url: str) -> dict:
    ydl_opts = {
        'quiet': True,
        'no_warnings': True,
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        info_dict = ydl.extract_info(url, download=False)
    return info_dict

def human_readable_time(seconds: int) -> str:
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    secs = seconds % 60
    return f"{hours:02d}:{minutes:02d}:{secs:02d}"

def download_audio(url: str, output_path=AUDIO_CACHE_DIR) -> str:
    ydl_opts = {
        'format': 'bestaudio/best',  # highest quality audio
        'outtmpl': f'{output_path}/%(title)s.%(ext)s',
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        # Extract info and download the file
        info_dict = ydl.extract_info(url, download=True)
        # Get the actual local file name
        filename = ydl.prepare_filename(info_dict)    
    return filename

def transcribe_audio(audio_file: str) -> str:
    device = "cuda" 
    batch_size = 4 # reduce if low on GPU mem
    compute_type = "float16" # change to "int8" if low on GPU mem (may reduce accuracy)
    model = whisperx.load_model("large-v2", device, compute_type=compute_type)
    audio = whisperx.load_audio(audio_file)
    result = model.transcribe(audio, batch_size=batch_size)
    return result['segments']

def transcribe_youtube_video(url: str) -> str:
    print("Downloading audio from YouTube with URL:", url)  
    filename = download_audio(url)
    print("Transcribing audio file:", filename)
    transcript_dict = transcribe_audio(filename)
    transcript = "\n".join([seg['text'] for seg in transcript_dict])
    return transcript

def main():
    st.title("TubeScribe")

    youtube_url = st.text_input("Enter a YouTube video URL")
    if youtube_url:
        try:
            info = get_video_info(youtube_url)
            title = info.get('title', 'Unknown Title')
            duration = info.get('duration', 0)
            uploader = info.get('uploader', 'Unknown Uploader')
            view_count = info.get('view_count', 'N/A')
            like_count = info.get('like_count', 'N/A')
            
            st.subheader("Video Metadata")
            st.write(f"**Title**: {title}")
            st.write(f"**Duration**: {human_readable_time(duration)}")
            st.write(f"**Uploader**: {uploader}")
            st.write(f"**View Count**: {view_count}")
            st.write(f"**Like Count**: {like_count}")

        except Exception as e:
            st.error(f"Failed to retrieve video info: {e}")

    if st.button("Transcribe"):
        if not youtube_url:
            st.warning("Please enter a valid YouTube URL first.")
        else:
            transcript = transcribe_youtube_video(youtube_url)
            st.success("Transcription complete! (Replace with real logic)")
            st.download_button(label="Download Transcript", 
                                data=transcript, 
                                file_name="transcript.txt")

main()