# OpenCV Video Overlay

Python command-line utility for adding a transparent PNG logo to a video and exporting the result as an AVI file.

## Features

- Alpha blending, including partially transparent pixels.
- Configurable logo position and dimensions.
- Input frame-rate preservation, with a 30 FPS fallback when metadata is unavailable.
- Validation of input video, logo channels, overlay bounds and output writer.
- Resource cleanup when processing finishes or fails.

## Installation

Use Python 3 and create a virtual environment:

```bash
git clone https://github.com/FastenSeatBeltWhileSeated/Opencv-add-logo-on-video.git
cd Opencv-add-logo-on-video
python -m venv .venv
```

Activate it with `source .venv/bin/activate` on Linux/macOS or `.venv\Scripts\Activate.ps1` on Windows PowerShell, then install:

```bash
python -m pip install -r requirements.txt
```

## Usage

Supply your own video and PNG logo with an alpha channel:

```bash
python logo.py --input input.avi --output output.avi --logo logo.png
```

Adjust the overlay:

```bash
python logo.py -i input.avi -o output.avi --logo logo.png --x 20 --y 20 --width 300 --height 100
```

| Argument | Default | Purpose |
| --- | --- | --- |
| `-i / --input` | Required | Source video |
| `-o / --output` | Required | Output AVI file |
| `--logo` | `Logo.png` | Four-channel PNG |
| `--x / --y` | `20 / 20` | Top-left position, in pixels |
| `--width / --height` | `300 / 100` | Resized logo dimensions |

The logo must fit completely inside the frame. Use a different output path: an existing output file may be overwritten.

## How blending works

For each pixel in the logo region:

```text
output = video × (1 − alpha) + logo × alpha
alpha = PNG alpha channel / 255
```

## Scope

This is a focused video-processing utility. It uses the MJPG codec and an AVI container, does not copy audio and does not include example input media.

The maintenance update corrects undefined variables in the original script, loads the logo once, preserves partial transparency and handles empty or invalid inputs.

## Validation

Verified with a generated AVI and PNG: frame count, dimensions, frame rate, overlay placement, partial-alpha blending, and invalid-input handling. Validation media is synthetic and is not an industrial deployment demonstration.

