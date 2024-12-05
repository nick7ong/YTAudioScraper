import argparse

from scraper import YouTubeAudioScraper


def main():
    parser = argparse.ArgumentParser(description="Download YouTube audio as WAV and convert to NumPy array.")
    parser.add_argument("yt_url", type=str, help="The YouTube video URL.")
    parser.add_argument("output_dir", type=str, help="Directory to save the WAV file.")

    args = parser.parse_args()

    try:
        # Initialize the scraper and download audio
        scraper = YouTubeAudioScraper(args.yt_url)
        numpy_data, sample_rate, output_path = scraper.download_audio(args.output_dir)

        # Print final results
        print(f"Audio data: {numpy_data.shape}, Sample rate: {sample_rate}")
        print(f"Audio saved to: {output_path}")
    except Exception as e:
        print(f"An error occurred: {str(e)}")


if __name__ == "__main__":
    main()
