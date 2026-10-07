import cv2
import numpy as np
import pytest

from video_overlay.core import load_logo, overlay_logo, process_video


@pytest.mark.parametrize("alpha,expected", [(0, (20,20,20)), (128, (10,10,130)), (255, (0,0,240))])
def test_alpha_blending_and_placement(alpha, expected):
    frame = np.full((40, 50, 3), 20, dtype=np.uint8)
    logo = np.full((10, 20, 4), (0, 0, 240, alpha), dtype=np.uint8)
    result = overlay_logo(frame, logo, 5, 5)
    np.testing.assert_array_equal(result[8, 8], expected)
    np.testing.assert_array_equal(result[0, 0], (20, 20, 20))


@pytest.mark.parametrize("x,y", [(-1,0), (0,-1), (45,0), (0,35)])
def test_out_of_bounds_rejected(x, y):
    with pytest.raises(ValueError):
        overlay_logo(np.zeros((40,50,3), dtype=np.uint8), np.zeros((10,20,4), dtype=np.uint8), x, y)


def test_logo_requires_alpha_channel(tmp_path):
    path = tmp_path / "rgb.png"
    cv2.imwrite(str(path), np.zeros((10,10,3), dtype=np.uint8))
    with pytest.raises(ValueError, match="channels"):
        load_logo(path, 10, 10)


def test_missing_logo_rejected(tmp_path):
    with pytest.raises(ValueError, match="Cannot read"):
        load_logo(tmp_path / "missing.png", 10, 10)


def test_invalid_image_arrays_rejected():
    frame = np.zeros((40,50,3), dtype=np.uint8)
    logo = np.zeros((10,20,4), dtype=np.uint8)
    with pytest.raises(ValueError, match="Frame"):
        overlay_logo(frame.astype(np.float32), logo, 0, 0)
    with pytest.raises(ValueError, match="Logo"):
        overlay_logo(frame, logo[:,:,:3], 0, 0)


def test_invalid_logo_dimensions_rejected(tmp_path):
    with pytest.raises(ValueError, match="positive"):
        load_logo(tmp_path / "logo.png", 0, 10)


def test_video_export_frame_count_fps_and_overlay(tmp_path):
    source, output, logo = tmp_path / "in.avi", tmp_path / "out.avi", tmp_path / "logo.png"
    writer = cv2.VideoWriter(str(source), cv2.VideoWriter_fourcc(*"MJPG"), 12, (160,120))
    assert writer.isOpened()
    for _ in range(6):
        writer.write(np.zeros((120,160,3), dtype=np.uint8))
    writer.release()
    cv2.imwrite(str(logo), np.full((10,20,4), (0,0,240,128), dtype=np.uint8))
    assert process_video(source, output, logo, 10,10,20,10) == 6
    reader = cv2.VideoCapture(str(output))
    try:
        assert int(reader.get(cv2.CAP_PROP_FRAME_COUNT)) == 6
        assert reader.get(cv2.CAP_PROP_FPS) == pytest.approx(12)
        success, frame = reader.read()
        assert success and frame.shape == (120,160,3)
        assert frame[15,18,2] > 90 and frame[15,18,0] < 30
    finally:
        reader.release()
    with pytest.raises(ValueError, match="different"):
        process_video(source, source, logo)
    with pytest.raises(ValueError, match="extension"):
        process_video(source, tmp_path / "out.mp4", logo)
    with pytest.raises(ValueError, match="Cannot open"):
        process_video(tmp_path / "missing.avi", output, logo)
