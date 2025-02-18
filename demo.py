""" Nicholas Tong
This is a simple demo script that demonstrates how to extract and process audio
from a YouTube video using Python.

The script follows these steps:
1. Takes a YouTube video URL as input.
2. Extracts the highest quality available audio stream (MP4 format).
3. Downloads the audio directly into an in-memory buffer.
4. Converts the MP4 audio into a WAV format using PyDub.
5. Reads the WAV data into a NumPy array for further processing.
6. Saves the processed audio as a WAV file.
"""

import os  # For creating directories and handling file paths
from io import BytesIO  # For creating in-memory binary buffers

import soundfile as sf  # For reading and writing audio files
from pydub import AudioSegment  # For audio format conversion
from pytubefix import YouTube  # For downloading YouTube videos

# YT URL --> YT Stream (m4a) --> Raw Binary Buffer (MP4) --> NumPy Array --> WAVE File


# Step 1: Input YouTube URL
yt_url = input("Enter YouTube URL: ")  # Prompt user to input the YouTube video URL

# Step 2: Initialize YouTube object
yt = YouTube(yt_url)  # Create a YouTube object for the given URL

# Step 3: Get audio stream
audio_stream = yt.streams.filter(only_audio=True)  # Filter streams to only include audio
audio_stream = yt.streams.filter(only_audio=True, file_extension='mp4')  # Further filter for MP4 audio streams
audio_stream = yt.streams.filter(only_audio=True,
                                 file_extension='mp4').last()  # Select the highest bitrate audio stream

# Step 4: Download audio to buffer
audio_buffer = BytesIO()  # Create an in-memory binary buffer to store the audio
yt.register_on_progress_callback(
    lambda stream, chunk, bytes_remaining: None)  # Register a callback for progress tracking (no-op here)
audio_stream.stream_to_buffer(audio_buffer)  # Stream the audio directly into the buffer
audio_buffer.seek(0)  # Reset buffer position to the beginning

# Step 5: Convert buffer to NumPy array
audio_segment = AudioSegment.from_file(audio_buffer, format="mp4")  # Read the audio buffer as an MP4 file
wav_buffer = BytesIO()  # Create another in-memory binary buffer for the WAV format
audio_segment.export(wav_buffer, format="wav")  # Export the audio to WAV format into the new buffer
wav_buffer.seek(0)  # Reset WAV buffer position to the beginning
numpy_data, sample_rate = sf.read(wav_buffer)  # Read the WAV buffer as NumPy array and get its sample rate

# Now we can do stuff with the audio array
# like lossy audio restoration or upmixing


# Step 6: Save audio to WAV file
output_dir = os.path.join("output")  # Define the output directory path
os.makedirs(output_dir, exist_ok=True)  # Create the output directory if it doesn't exist

output_path = os.path.join(output_dir, f"scraped_audio.wav")  # Define the path for the output WAV file

sf.write(output_path, numpy_data, sample_rate)  # Save the audio segment as a WAV file to the output path
