# YTAudioScraper
### Requirements
```bash
pip install -r requirements.txt
```

### How to Use
To run CLI script:
```bash
python cli_scraper.py <YT_URL> <OUTPUT_DIR>
```
To use YTAudioScraper() class in code:
```python
from scraper import YTAudioScraper
url = "<YT_URL>"
output_dir = "<OUTPUT_DIR>"

scraper = YouTubeAudioScraper(url)
data, sample_rate, output_path = scraper.download_audio(output_dir)
```
