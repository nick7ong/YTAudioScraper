# YTAudioScraper
This project enables users to scrape and download near-lossless 44.1kHz WAV audio from YouTube URLs. [Apollo](https://github.com/JusperLee/Apollo) is used to reconstruct and restore the missing high-frequency content (>16kHz) from the lossy MP4 compression.

### Environment Setup and Requirements
```bash
# venv (for CPU w/o enhancer)
python3 -m venv <env-name>
source <env-name>/bin/activate
pip install -r requirements.txt

# miniconda3 (with cuda/GPU support)
conda create --name <env-name> python=3.10
conda activate <env-name>
pip install -r requirements.txt
```

### How to Use
To run CLI script:
```bash
python yt_scraper.py <YT_URL> <OUTPUT_DIR> --enhance --weights <CKPT_FILE>
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
Pre-trained model weights:
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
@inproceedings{li2025apollo,
  title={Apollo: Band-sequence Modeling for High-Quality Music Restoration in Compressed Audio},
  author={Li, Kai and Luo, Yi},
  booktitle={IEEE International Conference on Acoustics, Speech and Signal Processing (ICASSP)},
  year={2025},
  organization={IEEE}
}
```
