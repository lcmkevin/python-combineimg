# Build EXE from combineimgv3.py (Windows x64)

This guide explains how to generate a self-contained Windows `.exe` from the Python GUI app in this repository.

## Prerequisites

1. Python 3.11+ (64-bit) installed
2. `pip` package manager
3. Git clone repository

## Install required Python packages

```bash
pip install pillow pyinstaller
```

## Build a single-file executable

From repository root `/workspaces/python-combineimg`:

```bash
pyinstaller --onefile --windowed --name combineimgv3 combineimgv3.py
```

- `--onefile`: single executable
- `--windowed`: no console window (GUI app)
- `--name combineimgv3`: output file name

## Build with icon (optional)

```bash
pyinstaller --onefile --windowed --name combineimgv3 --icon=app.ico combineimgv3.py
```

## Advanced options

- Add file data (e.g., README, docs):
  ```bash
  pyinstaller --onefile --windowed --add-data "README.md;." combineimgv3.py
  ```
- Clean previous build artifacts:
  ```bash
  pyinstaller --onefile --windowed --clean combineimgv3.py
  ```

## Output location

`dist\combineimgv3.exe`

## Run and verify

- Double-click `dist\combineimgv3.exe` on Windows
- Or run:
  ```bash
  dist\combineimgv3.exe
  ```

## Notes

- Existing app supports image formats and PDF import/export through Pillow.
- If PDF page-handling is missing on a system, confirm Pillow is installed and the app can read the PDF file.
- Use matching Python bitness (x64) to generate a x64 executable.
