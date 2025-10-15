import os
import re
from io import BytesIO

import soundfile as sf
from colorama import Fore, Style, init
from pydub import AudioSegment
from pytubefix import YouTube
from tqdm import tqdm

# Initialize colorama
init(autoreset=True)


class YouTubeAudioScraper:
    def __init__(self, url):
        self.url = url
        self.yt = YouTube(url)
        self.audio_buffer = None  # Store the audio_path buffer to avoid re-downloading
        self.numpy_data = None  # Store NumPy array data for reuse
        self.sample_rate = None
        print(f"{Fore.CYAN}Initialized YouTube scraper for URL: {url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Video title: {self.yt.title}{Style.RESET_ALL}")
        self._buffer_audio()  # Ensure the buffer is initialized during setup

    def _get_audio_stream(self):
        """Retrieve the audio_path stream from the YouTube video."""
        print(f"{Fore.YELLOW}Fetching audio_path stream...{Style.RESET_ALL}")
        stream_query = self.yt.streams.filter(only_audio=True, file_extension='mp4')  # Ffmpeg only supports m4a/aac
        audio_stream = stream_query.last()  # Last stream is highest bitrate
        if audio_stream:
            print(f"{Fore.GREEN}Audio stream retrieved successfully.{Style.RESET_ALL}")
        else:
            raise ValueError(f"{Fore.RED}Failed to retrieve audio_path stream.{Style.RESET_ALL}")
        return audio_stream

    def _buffer_audio(self):
        """Buffer the audio_path stream into a BytesIO object."""
        if self.audio_buffer:
            print(f"{Fore.GREEN}Audio already downloaded. Using cached buffer.{Style.RESET_ALL}")
            return self.audio_buffer

        audio_stream = self._get_audio_stream()
        buffer = BytesIO()

        if not audio_stream:
            raise ValueError("Audio stream not found.")

        total_size = audio_stream.filesize

        with tqdm(
                total=total_size,
                unit="B",
                unit_scale=True,
                desc="Downloading audio_path from URL",
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {unit}",
        ) as pbar:
            def progress_hook(stream, chunk, bytes_remaining):
                pbar.update(len(chunk))

            self.yt.register_on_progress_callback(progress_hook)
            audio_stream.stream_to_buffer(buffer)

        buffer.seek(0)
        self.audio_buffer = buffer
        return buffer

    def _convert_to_numpy(self):
        """Convert the audio_path buffer to a NumPy array and store the result."""
        if self.numpy_data is not None and self.sample_rate is not None:
            print(f"{Fore.GREEN}NumPy data already converted. Reusing cached data.{Style.RESET_ALL}")
            return self.numpy_data, self.sample_rate

        buffer = self._get_fresh_buffer()

        with tqdm(
                total=100,
                desc="Converting audio_path to NumPy array",
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {unit}",
        ) as pbar:
            audio_segment = AudioSegment.from_file(buffer, format="mp4")
            wav_buffer = BytesIO()
            audio_segment.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            pbar.update(100)

        self.numpy_data, self.sample_rate = sf.read(wav_buffer)
        return self.numpy_data, self.sample_rate

    def _get_fresh_buffer(self):
        """Create a fresh copy of the audio_path buffer for each use."""
        if not self.audio_buffer:
            raise ValueError("Audio buffer is not initialized.")
        new_buffer = BytesIO(self.audio_buffer.getvalue())
        new_buffer.seek(0)
        return new_buffer

    def download_audio(self, destination_dir, format="wav"):
        """
        Convert the YouTube audio_path to NumPy, then save as a WAV file.

        Args:
            destination_dir (str): Path to the directory where the file will be saved.
            format (str, optional): The output format of the audio file (i.e. "wav" or "mp3").

        Returns:
            tuple: (numpy_data, sample_rate, str) - NumPy data, sample rate, and the file path.
        """
        # Ensure NumPy conversion happens before saving
        numpy_data, sample_rate = self._convert_to_numpy()

        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f"{Fore.GREEN}Created output directory: {destination_dir}{Style.RESET_ALL}")

        sanitized_title = re.sub(r"[\/| ]|[\s-]*-[\s-]*", "_", self.yt.title)
        sanitized_title = re.sub(r"_+", "_", sanitized_title)
        output_path = os.path.join(destination_dir, f"{sanitized_title}.{format}")

        with tqdm(
                total=100,
                desc=f"Saving audio_path to {format} file",
                bar_format="{desc}: {percentage:3.0f}%|{bar}| {n_fmt}/{total_fmt} {unit}",
        ) as pbar:
            buffer = self._get_fresh_buffer()
            audio_segment = AudioSegment.from_file(buffer, format="mp4")
            audio_segment.export(output_path, format=format)
            pbar.update(100)

        print(f"{Fore.GREEN}Download complete.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}File saved to: {output_path}{Style.RESET_ALL}")
        return numpy_data, sample_rate, output_path


if __name__ == "__main__":
    yt_url = input("URL > ")
    output_dir = os.path.join("..", "output")
    format = "mp3"

    try:
        # Initialize the scraper and execute its methods
        scraper = YouTubeAudioScraper(yt_url)
        scraper.download_audio(output_dir, format=format)
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
