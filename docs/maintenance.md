# Maintenance and structure

The original root `logo.py` script has been split into:

- `src/video_overlay/core.py`: reusable image and video functions.
- `src/video_overlay/cli.py`: argument parsing and user-facing errors.
- `src/video_overlay/__main__.py`: module execution.
- `examples/synthetic_demo.py`: input video, PNG and preview generation.
- `tests/test_overlay.py`: alpha, placement and export checks.

Use `video-overlay` or `python -m video_overlay` after installation. The earlier script remains in Git history.

Dependencies and console commands are defined in `pyproject.toml`, replacing `requirements.txt`.

The utility preserves source FPS when available, exports MJPG AVI and does not copy audio. Overlay pixels are blended using the PNG alpha channel:

```text
output = video × (1 − alpha) + logo × alpha
alpha = PNG alpha / 255
```

The logo must fit completely inside the frame. Out-of-bounds positions, missing inputs, PNGs without alpha and unsupported output extensions are rejected.
