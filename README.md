# stems-demucs

A Python project for audio source separation using Demucs.

## Getting Started on Windows

1. **Install uv** (Python package manager):
   ```powershell
   powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
   ```

2. **Clone and run**:
   ```bash
   git clone <your-repo-url>
   cd stems-demucs
   uv run python -m demucs -n htdemucs_ft -o output/ "path/to/your/audio/file.mp3"
   ```

The separated stems will be saved in the `output/` directory.

## Dependencies

- Python 3.10+
- PyTorch, Demucs, librosa, and other audio processing libraries (automatically installed via uv)