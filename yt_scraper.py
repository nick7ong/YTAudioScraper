import argparse
import os

from colorama import Fore, Style

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
    parser.add_argument("--enhance", action="store_true", help="Lossy audio restoration using Apollo.")
    parser.add_argument("--weights", type=str, nargs="?", default="enhancer/weights/apollo_model_uni.ckpt")

    args = parser.parse_args()

    os.makedirs(args.output_dir, exist_ok=True)

    try:
        # Initialize the scraper and download audio_path
        scraper = YouTubeAudioScraper(args.yt_url)
        numpy_data, sample_rate, output_path = scraper.download_audio(args.output_dir)

        if args.enhance:
            import enhancer
            print(f"{Fore.YELLOW}Enhance={args.enhance}{Style.RESET_ALL}")
            print(f"{Fore.YELLOW}Model weights={args.weights}{Style.RESET_ALL}")
            enhanced_filename = f"enhanced_{os.path.basename(output_path)}"
            enhanced_path = os.path.join(args.output_dir, enhanced_filename)
            enhancer.process_audio(output_path, enhanced_path, args.weights)

    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
