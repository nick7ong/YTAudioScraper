import os
import soundfile as sf

from pytube import YouTube
from pydub import AudioSegment
from io import BytesIO


def yt_to_narray(url):
    yt = YouTube(url)

    # Get the audio stream
    stream_query = yt.streams.filter(only_audio=True)
    audio_stream = stream_query.get_audio_only()

    # Buffer the audio
    buffer = BytesIO()
    audio_stream.stream_to_buffer(buffer)
    buffer.seek(0)

    # Write to wav file
    audio_segment = AudioSegment.from_file(buffer, format="mp4")
    wav_buffer = BytesIO()
    audio_segment.export(wav_buffer, format="wav")
    wav_buffer.seek(0)

    audio, fs = sf.read(wav_buffer)

    return audio, fs, yt


def download_youtube_audio(url, destination_dir):
    """Function to download YouTube audio to wav file."""
    yt = YouTube(url)

    # Get the audio stream
    stream_query = yt.streams.filter(only_audio=True)
    audio_stream = stream_query.get_audio_only()

    # Buffer the audio
    buffer = BytesIO()
    audio_stream.stream_to_buffer(buffer)
    buffer.seek(0)

    # Prepare output directory
    if not os.path.exists(destination_dir):
        os.makedirs(destination_dir)

    # Write to wav file
    audio_segment = AudioSegment.from_file(buffer, format="mp4")
    output_path = os.path.join(destination_dir, f"{yt.title.replace('/', '_').replace('|', '_')}.wav")
    audio_segment.export(output_path, format="wav")

    return output_path
