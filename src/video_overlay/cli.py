"""Command-line interface for PNG video overlays."""

import argparse

import cv2

from .core import process_video

def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", required=True, help="Input video path")
    parser.add_argument("-o", "--output", required=True, help="Output AVI path (MJPG)")
    parser.add_argument("--logo", default="Logo.png", help="Transparent PNG (default: Logo.png)")
    parser.add_argument("--x", type=int, default=20, help="Horizontal offset in pixels")
    parser.add_argument("--y", type=int, default=20, help="Vertical offset in pixels")
    parser.add_argument("--width", type=int, default=300, help="Logo width in pixels")
    parser.add_argument("--height", type=int, default=100, help="Logo height in pixels")
    args = parser.parse_args(argv)
    try:
        frames = process_video(args.input, args.output, args.logo, args.x, args.y,
                               args.width, args.height)
    except (ValueError, OSError, cv2.error) as error:
        parser.error(str(error))
    print(f"Processed {frames} frames. Output: {args.output}")

