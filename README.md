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

Informative resources on YouTube audio stream quality: 
- [YT Audio Quality Analysis](https://www.audiomisc.co.uk/YouTube/SpotTheDifference.html)
- [YT Stream Format Codes](https://gist.github.com/sidneys/7095afe4da4ae58694d128b1034e01e2)

### Citations
```text
@article{li2024apollo,
  title={Apollo: Band-sequence Modeling for High-Quality Music Restoration in Compressed Audio},
  author={Li, Kai and Luo, Yi},
  journal={xxxxxx},
  year={2024}
}
```