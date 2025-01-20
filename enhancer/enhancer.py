import argparse

import librosa
import numpy as np
import soundfile as sf
import torch
from tqdm import tqdm

from apollo import Apollo


def load_audio(file_path):
    audio, samplerate = librosa.load(file_path, mono=False, sr=44100)
    print(f'INPUT audio_path.shape = {audio.shape} | samplerate = {samplerate}')
    # audio_path = dBgain(audio_path, -6)
    return torch.from_numpy(audio), samplerate


def save_audio(file_path, audio, fs=44100):
    sf.write(file_path, audio, fs)


def _getWindowingArray(window_size, fade_size):
    # IMPORTANT NOTE :
    # no fades here in the end, only removing the failed ending of the chunk
    fadein = torch.linspace(1, 1, fade_size)
    fadeout = torch.linspace(0, 0, fade_size)
    window = torch.ones(window_size)
    window[-fade_size:] *= fadeout
    window[:fade_size] *= fadein
    return window


def enchance(model, audio_path, device):
    test_data, samplerate = load_audio(audio_path)
    test_data = test_data.to(device)  # Move audio data to the device

    C = 10 * samplerate  # chunk_size seconds to samples
    N = 2
    step = C // N
    fade_size = 3 * 44100  # 3 seconds
    print(f"N = {N} | C = {C} | step = {step} | fade_size = {fade_size}")

    border = C - step

    # Handle mono inputs correctly
    if len(test_data.shape) == 1:
        test_data = test_data.unsqueeze(0)

    # Pad the input if necessary
    if test_data.shape[1] > 2 * border and (border > 0):
        test_data = torch.nn.functional.pad(test_data, (border, border), mode='reflect')

    windowingArray = _getWindowingArray(C, fade_size).to(device)  # Move to device

    result = torch.zeros((1,) + tuple(test_data.shape), dtype=torch.float32, device=device)
    counter = torch.zeros((1,) + tuple(test_data.shape), dtype=torch.float32, device=device)

    i = 0
    progress_bar = tqdm(total=test_data.shape[1], desc="Processing audio_path chunks", leave=False)

    while i < test_data.shape[1]:
        part = test_data[:, i:i + C]
        length = part.shape[-1]
        if length < C:
            if length > C // 2 + 1:
                part = torch.nn.functional.pad(input=part, pad=(0, C - length), mode='reflect')
            else:
                part = torch.nn.functional.pad(input=part, pad=(0, C - length, 0, 0), mode='constant', value=0)

        chunk = part.unsqueeze(0)  # Prepare for model input
        with torch.no_grad():
            out = model(chunk).squeeze(0).squeeze(0)

        window = windowingArray.clone()  # Use clone to avoid modifying the original tensor
        if i == 0:  # First audio_path chunk, no fadein
            window[:fade_size] = 1
        elif i + C >= test_data.shape[1]:  # Last audio_path chunk, no fadeout
            window[-fade_size:] = 1

        result[..., i:i + length] += out[..., :length] * window[..., :length]
        counter[..., i:i + length] += window[..., :length]

        i += step
        progress_bar.update(step)

    progress_bar.close()

    final_output = result / counter
    final_output = final_output.squeeze(0).cpu().numpy()  # Move final output back to CPU for saving
    np.nan_to_num(final_output, copy=False, nan=0.0)

    # Remove padding if added earlier
    if test_data.shape[1] > 2 * border and (border > 0):
        final_output = final_output[..., border:-border]

    return samplerate, final_output.T


def main(input_wav, output_wav, checkpoint_file):
    device = "cuda" if torch.cuda.is_available() else "cpu"

    checkpoint = torch.load(checkpoint_file, map_location=device)
    if ".bin" in checkpoint_file:
        sr = checkpoint['model_args'].sr
        win = checkpoint['model_args'].win
        feature_dim = checkpoint['model_args'].feature_dim
        layer = checkpoint['model_args'].layer
    elif ".ckpt" in checkpoint_file:  # Hard-coded values for the uni model
        sr = 44100
        win = 20
        feature_dim = 384
        layer = 6

    model = Apollo(
        sr=sr,
        win=win,
        feature_dim=feature_dim,
        layer=layer
    ).to(device)

    model.load_state_dict(checkpoint['state_dict'])

    with torch.no_grad():
        fs, output = enchance(model, input_wav, device)
    save_audio(output_wav, output, fs)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Audio Inference Script")
    parser.add_argument("--in_wav", type=str, required=True, help="Path to input wav file")
    parser.add_argument("--out_wav", type=str, required=True, help="Path to output wav file")
    parser.add_argument("--weights", type=str, required=True, help="Path to weights file")
    args = parser.parse_args()

    main(args.in_wav, args.out_wav, args.weights)
    # main("../output/128kbps.wav", "../output/upscaled_128kbps.wav", "weights/apollo.bin")
