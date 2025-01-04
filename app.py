import streamlit as st
import whisperx

def main():
    st.title("TubeScribe")
    # 1. Input for YouTube URL
    youtube_url = st.text_input("Enter a YouTube video URL")

    if st.button("Transcribe"):
        # 2. Call your transcription function using whisperx
        transcript = transcribe_youtube_video(youtube_url)
        st.success("Transcription complete!")
        
        # 3. Provide a downloadable file
        st.download_button(label="Download Transcript", 
                           data=transcript, 
                           file_name="transcript.txt")

def transcribe_youtube_video(url):
    # your logic to download audio, run whisperx, etc.
    # return the transcript text
    return "Sample transcript text for now!"

# if __name__ == "__main__":
#     main()

main()