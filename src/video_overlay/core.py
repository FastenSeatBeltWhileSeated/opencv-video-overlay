"""Add a transparent PNG overlay to a video using OpenCV."""

from pathlib import Path

import cv2
import numpy as np


def load_logo(path, width, height):
    if width <= 0 or height <= 0:
        raise ValueError("Logo dimensions must be positive")
    image = cv2.imread(str(path), cv2.IMREAD_UNCHANGED)
    if image is None:
        raise ValueError(f"Cannot read logo: {path}")
    if image.ndim != 3 or image.shape[2] != 4:
        raise ValueError("Logo must have four channels (BGRA), including transparency")
    return cv2.resize(image, (width, height))


def overlay_logo(frame, logo, x, y):
    """Blend a BGRA logo into a BGR frame in place, preserving partial alpha."""
    if (not isinstance(frame, np.ndarray) or frame.dtype != np.uint8
            or frame.ndim != 3 or frame.shape[2] != 3 or frame.size == 0):
        raise ValueError("Frame must be a nonempty uint8 BGR image")
    if (not isinstance(logo, np.ndarray) or logo.dtype != np.uint8
            or logo.ndim != 3 or logo.shape[2] != 4 or logo.size == 0):
        raise ValueError("Logo must be a nonempty uint8 BGRA image")
    height, width = logo.shape[:2]
    if x < 0 or y < 0 or x + width > frame.shape[1] or y + height > frame.shape[0]:
        raise ValueError("Logo position and dimensions must fit inside the video frame")
    region = frame[y:y + height, x:x + width]
    alpha = logo[:, :, 3:4].astype(np.float32) / 255.0
    blended = region.astype(np.float32) * (1.0 - alpha) + logo[:, :, :3] * alpha
    region[:] = np.rint(blended).astype(np.uint8)
    return frame


def process_video(input_path, output_path, logo_path, x=20, y=20, width=300, height=100):
    if Path(input_path).resolve() == Path(output_path).resolve():
        raise ValueError("Input and output paths must be different")
    if Path(output_path).suffix.lower() != ".avi":
        raise ValueError("Output must use the .avi extension (MJPG codec)")
    logo = load_logo(logo_path, width, height)
    capture = cv2.VideoCapture(str(input_path))
    writer = None
    count = 0
    try:
        if not capture.isOpened():
            raise ValueError(f"Cannot open input video: {input_path}")
        fps = capture.get(cv2.CAP_PROP_FPS)
        if not np.isfinite(fps) or fps <= 0:
            fps = 30.0
        while True:
            grabbed, frame = capture.read()
            if not grabbed:
                break
            frame = overlay_logo(frame, logo, x, y)
            if writer is None:
                frame_height, frame_width = frame.shape[:2]
                writer = cv2.VideoWriter(str(output_path), cv2.VideoWriter_fourcc(*"MJPG"),
                                         fps, (frame_width, frame_height))
                if not writer.isOpened():
                    raise ValueError(f"Cannot open output video: {output_path}; use an .avi file")
            writer.write(frame)
            count += 1
        if count == 0:
            raise ValueError("Input video contains no readable frames")
        return count
    finally:
        capture.release()
        if writer is not None:
            writer.release()

