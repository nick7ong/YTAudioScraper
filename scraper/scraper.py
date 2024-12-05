import os
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
        self.audio_buffer = None  # Store the audio buffer to avoid re-downloading
        self.numpy_data = None  # Store NumPy array data for reuse
        self.sample_rate = None
        print(f"{Fore.CYAN}Initialized YouTube scraper for URL: {url}{Style.RESET_ALL}")
        print(f"{Fore.CYAN}Video title: {self.yt.title}{Style.RESET_ALL}")
        self._buffer_audio()  # Ensure the buffer is initialized during setup

    def _get_audio_stream(self):
        """Retrieve the audio stream from the YouTube video."""
        print(f"{Fore.YELLOW}Fetching audio stream...{Style.RESET_ALL}")
        stream_query = self.yt.streams.filter(only_audio=True)
        audio_stream = stream_query.first()
        if audio_stream:
            print(f"{Fore.GREEN}Audio stream retrieved successfully.{Style.RESET_ALL}")
        else:
            raise ValueError(f"{Fore.RED}Failed to retrieve audio stream.{Style.RESET_ALL}")
        return audio_stream

    def _buffer_audio(self):
        """Buffer the audio stream into a BytesIO object."""
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
                desc="Downloading audio from URL",
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
        """Convert the audio buffer to a NumPy array and store the result."""
        if self.numpy_data is not None and self.sample_rate is not None:
            print(f"{Fore.GREEN}NumPy data already converted. Reusing cached data.{Style.RESET_ALL}")
            return self.numpy_data, self.sample_rate

        buffer = self._get_fresh_buffer()

        with tqdm(
                total=100,
                desc="Converting audio to NumPy array",
                bar_format="{desc}: {percentage:3.0f}%|{bar}|",
        ) as pbar:
            audio_segment = AudioSegment.from_file(buffer, format="mp4")
            wav_buffer = BytesIO()
            audio_segment.export(wav_buffer, format="wav")
            wav_buffer.seek(0)
            pbar.update(100)

        self.numpy_data, self.sample_rate = sf.read(wav_buffer)
        return self.numpy_data, self.sample_rate

    def _get_fresh_buffer(self):
        """Create a fresh copy of the audio buffer for each use."""
        if not self.audio_buffer:
            raise ValueError("Audio buffer is not initialized.")
        new_buffer = BytesIO(self.audio_buffer.getvalue())
        new_buffer.seek(0)
        return new_buffer

    def download_audio(self, destination_dir):
        """
        Convert the YouTube audio to NumPy, then save as a WAV file.

        Args:
            destination_dir (str): Path to the directory where the file will be saved.

        Returns:
            tuple: (numpy_data, sample_rate, str) - NumPy data, sample rate, and the file path.
        """
        # Ensure NumPy conversion happens before saving
        numpy_data, sample_rate = self._convert_to_numpy()

        # Ensure the destination directory exists
        if not os.path.exists(destination_dir):
            os.makedirs(destination_dir)
            print(f"{Fore.GREEN}Created output directory: {destination_dir}{Style.RESET_ALL}")

        sanitized_title = self.yt.title.replace("/", "_").replace("|", "_").replace(" ", "_")
        output_path = os.path.join(destination_dir, f"{sanitized_title}.wav")

        with tqdm(
                total=100,
                desc="Saving audio to WAV file",
                bar_format="{desc}: {percentage:3.0f}%|{bar}|",
        ) as pbar:
            buffer = self._get_fresh_buffer()
            audio_segment = AudioSegment.from_file(buffer, format="mp4")
            audio_segment.export(output_path, format="wav")
            pbar.update(100)

        print(f"{Fore.GREEN}Download complete.{Style.RESET_ALL}")
        print(f"{Fore.GREEN}File saved to: {output_path}{Style.RESET_ALL}")
        return numpy_data, sample_rate, output_path


if __name__ == "__main__":
    yt_url = "https://youtu.be/SXQeyudFe-g"
    output_dir = os.path.join("..", "output")

    try:
        # Initialize the scraper and execute its methods
        scraper = YouTubeAudioScraper(yt_url)
        scraper.download_audio(output_dir)
    except Exception as e:
        print(f"{Fore.RED}An error occurred: {str(e)}{Style.RESET_ALL}")
