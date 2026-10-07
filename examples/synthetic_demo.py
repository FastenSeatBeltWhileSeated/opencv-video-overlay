"""Create input media and a preview without any external assets."""

from pathlib import Path

import cv2
import numpy as np

from video_overlay.core import overlay_logo, process_video


def main():
    root = Path(__file__).resolve().parents[1]
    generated = root / "examples" / "generated"
    generated.mkdir(parents=True, exist_ok=True)
    assets = root / "docs" / "assets"
    assets.mkdir(parents=True, exist_ok=True)
    source, output, logo_path = generated / "input.avi", generated / "output.avi", generated / "logo.png"
    logo = np.zeros((40, 100, 4), dtype=np.uint8)
    logo[:, :, :3] = (40, 160, 250)
    logo[:, :50, 3] = 128
    logo[:, 50:, 3] = 255
    cv2.putText(logo, "DEMO", (9, 27), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255,255,255,255), 2)
    if not cv2.imwrite(str(logo_path), logo):
        raise RuntimeError("Cannot create PNG")
    writer = cv2.VideoWriter(str(source), cv2.VideoWriter_fourcc(*"MJPG"), 12, (320,240))
    if not writer.isOpened():
        raise RuntimeError("Cannot create synthetic video")
    try:
        for index in range(36):
            frame = np.full((240,320,3), (90,60,30), dtype=np.uint8)
            cv2.circle(frame, (60 + index * 3, 150), 30, (150,220,100), -1)
            writer.write(frame)
    finally:
        writer.release()
    process_video(source, output, logo_path, 20,20,100,40)
    overlaid = overlay_logo(frame.copy(), logo, 20,20)
    preview = np.zeros((270,640,3), dtype=np.uint8)
    preview[30:, :320], preview[30:, 320:] = frame, overlaid
    for x, label in ((10, "Synthetic input"), (330, "PNG overlay: partial + full alpha")):
        cv2.putText(preview, label, (x,21), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255), 1)
    if not cv2.imwrite(str(assets / "synthetic-overlay.png"), preview):
        raise RuntimeError("Cannot create preview")
    print(f"Input: {source}\nLogo: {logo_path}\nOutput: {output}")


if __name__ == "__main__":
    main()
