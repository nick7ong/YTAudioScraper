import argparse

import torch
import torchaudio

from apollo import Apollo


def load_audio(file_path, device="cuda"):
    audio, samplerate = torchaudio.load(file_path)
    return audio.unsqueeze(0).to(device)  # [1, 1, samples]


def save_audio(file_path, audio, samplerate=44100, device="cuda"):
    audio = audio.squeeze(0).to(device)
    torchaudio.save(file_path, audio, samplerate)


def main(input_wav, output_wav, checkpoint_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    model = Apollo(sr=44100, win=20, feature_dim=384, layer=6).to(device)
    checkpoint = torch.load(checkpoint_file)
    model.load_state_dict(checkpoint['state_dict'])
    test_data = load_audio(input_wav, device=device)
    with torch.no_grad():
        out = model(test_data)
    save_audio(output_wav, out, device=device)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Inference Script")
    parser.add_argument("--in_wav", type=str, required=True, help="Path to input wav file")
    parser.add_argument("--out_wav", type=str, required=True, help="Path to output wav file")
    args = parser.parse_args()

    main(args.in_wav, args.out_wav, "weights/apollo_model_uni.ckpt")
    # main("../output/128kbps.wav", "../output/upscaled_128kbps.wav", "weights/apollo_model_uni.ckpt")
