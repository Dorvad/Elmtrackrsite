# Product-film source

`elmtrackr-tour-original.mp4` is the original 1080×1920, 30 fps master. The
production-served encodes in `assets/` are 720×1280 at 24 fps:

- H.264/AAC MP4: x264 High Profile, CRF 26, slow preset, 80 kb/s AAC, and
  `+faststart` metadata.
- VP9/Opus WebM: VP9 CRF 36 and 64 kb/s Opus.

The original remains here so future encodes start from the master rather than
from an already compressed production derivative. The build and deploy steps
exclude the complete `docs/` directory.
