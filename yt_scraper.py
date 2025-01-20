import argparse
import os

import enhancer
from scraper import YouTubeAudioScraper


def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio_path as WAV and convert to NumPy array.")
    parser.add_argument("yt_url", type=str, help="The YouTube video URL.")
    parser.add_argument(
        "output_dir",
        type=str,
        nargs="?",  # Make this argument optional
        default="output",  # Set default value to 'output'
        help="Directory to save the WAV file. Defaults to 'output'."
    )
    parser.add_argument("--enhance", type=bool, default=False, help="Lossy audio restoration using Apollo.")
    parser.add_argument("--weights", type=str, nargs="?", default="enhancer/weights/apollo_model_uni.ckpt")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    try:
        # Initialize the scraper and download audio_path
        scraper = YouTubeAudioScraper(args.yt_url)
        numpy_data, sample_rate, output_path = scraper.download_audio(args.output_dir)

        # Print final results
        print(f"Audio data: {numpy_data.shape}, Sample rate: {sample_rate}")
        print(f"Audio saved to: {output_path}")

        if args.enhance:
            enhancer.process_audio(output_path, output_path, args.weights)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
