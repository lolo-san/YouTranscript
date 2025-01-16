# YouTranscript
Paste a YouTube link, click ‘Transcribe’, and download the transcript.

## Description
YouTranscript is a Streamlit application that allows users to transcribe YouTube videos. It uses several dependencies to achieve this functionality:
- `torch` and `torchaudio`: Used for audio processing and transcription.
- `whisperx`: A library for speech recognition and transcription.
- `yt-dlp`: A YouTube downloader library used to fetch video metadata, thumbnails, and audio tracks.
- `streamlit`: A framework for creating interactive web applications.

## Installation and Setup
To install the necessary dependencies, run the following commands:

```bash
pip install torch==2.3.1 torchaudio==2.3.1 --index-url https://download.pytorch.org/whl/cu118

pip install git+https://github.com/m-bain/whisperx.git@49161922461871e6732fbe1aeb20fc1d4cccc9df

pip install -r requirements.txt
```

## Running the Application
To run the application locally, use the following command:

```bash
make run
```

This will start the Streamlit app, and you can access it in your web browser.

## Running Tests
To run the tests, use the following command:

```bash
make test
```

This will execute the tests using `pytest`.

## Linting the Code
To lint the code, use the following command:

```bash
make lint
```

This will format the code using `black` and check for linting errors using `pylint`.

## Cleaning Temporary Files
To clean the temporary files in the `tmp` directory, use the following command:

```bash
make clean
```
