import argparse
import os
from io import BytesIO

import soundfile as sf
from pydub import AudioSegment
from pytube import YouTube


class YouTubeAudioScraper:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)

    def _get_audio_stream(self):
        """Retrieve the audio stream from the YouTube video."""
        stream_query = self.yt.streams.filter(only_audio=True)
        return stream_query.get_audio_only()

    def _buffer_audio(self):
        """Buffer the audio stream into a BytesIO object."""
        audio_stream = self._get_audio_stream()
        buffer = BytesIO()
        audio_stream.stream_to_buffer(buffer)
        buffer.seek(0)
        return buffer

    def to_numpy_array(self):
        """
        Convert YouTube audio to a NumPy array and sample rate.

        Returns:
            tuple: (audio_data, sample_rate, YouTube object)
        """
        buffer = self._buffer_audio()

        # Convert to wav format and read as numpy array
        audio_segment = AudioSegment.from_file(buffer, format="mp4")
        wav_buffer = BytesIO()
        audio_segment.export(wav_buffer, format="wav")
        wav_buffer.seek(0)

        audio, sample_rate = sf.read(wav_buffer)
        return audio, sample_rate, self.yt

    def download_audio(self, destination_dir):
        """
        Download the YouTube audio as a WAV file to the specified directory.

        Args:
            destination_dir (str): Path to the directory where the file will be saved.

        Returns:
            str: The path to the saved WAV file.
        """
        buffer = self._buffer_audio()

        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)

        # Convert to wav format and save to file
        audio_segment = AudioSegment.from_file(buffer, format="mp4")
        sanitized_title = self.yt.title.replace('/', '_').replace('|', '_')
        output_path = os.path.join(destination_dir, f"{sanitized_title}.wav")
        audio_segment.export(output_path, format="wav")

        return output_path


def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio as WAV or convert to NumPy array.")
    parser.add_argument("url", type=str, help="The YouTube video URL.")
    parser.add_argument("destination_dir", type=str, help="Directory to save the WAV file.")

    args = parser.parse_args()

    # Initialize the processor
    scraper = YouTubeAudioScraper(args.url)

    # Convert to NumPy array
    audio_data, sample_rate, yt = scraper.to_numpy_array()
    print(f"Audio sample rate: {sample_rate}")
    print(f"Video title: {yt.title}")

    # Download audio
    output_path = scraper.download_audio(args.destination_dir)
    print(f"Audio saved to: {output_path}")


if __name__ == "__main__":
    main()
