# YTAudioScraper
This project enables users to download WAV audio files from YouTube URLs and applies the [Apollo](https://github.com/JusperLee/Apollo) deep learning model to reconstruct and restore high-frequency content above 16kHz lost due to lossy MP4 compression. 
By combining audio scraping and advanced audio enhancement, it delivers improved audio quality for applications requiring near-lossless sound fidelity.

### Environment Setup and Requirements
```bash
conda create --name <env-name> python=3.10
conda activate <env-name>
pip install -r requirements.txt
```

### How to Use
To run CLI script:
```bash
python yt_scraper.py <YT_URL> <OUTPUT_DIR> --enhance True
```
To use YTAudioScraper() class in code:
```python
import enhancer
from scraper import YTAudioScraper

url = "<YT_URL>"
output_dir = "<OUTPUT_DIR>"
weights = "<WEIGHTS_PATH>"  # .bin or .ckpt

scraper = YouTubeAudioScraper(url)
data, sample_rate, output_path = scraper.download_audio(output_dir)

# Optionally restore >16kHz content with enhancer
enhancer.process_audio(input_path, output_path, weights)
```

### Resources
Enhancer model weights:
```bash
cd enhancer/weights
wget 'https://huggingface.co/JusperLee/Apollo/resolve/main/pytorch_model.bin'
wget 'https://huggingface.co/jarredou/lew_apollo_vocal_enhancer/resolve/main/apollo_model.ckpt'
wget 'https://huggingface.co/jarredou/lew_apollo_vocal_enhancer/resolve/main/apollo_model_v2.ckpt'
wget 'https://github.com/deton24/Lew-s-vocal-enhancer-for-Apollo-by-JusperLee/releases/download/uni/apollo_model_uni.ckpt'
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