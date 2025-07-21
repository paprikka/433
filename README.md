# Masked Font Generator

Generate masked fonts where all characters appear as dots, preserving text structure while hiding content.

## Requirements

- Python 3.8+
- FontForge (system dependency)

## Setting up FontForge

**macOS:**
```bash
# Install FontForge with Python support
brew install fontforge

# Add FontForge Python module to your environment
export PYTHONPATH="/opt/homebrew/lib/python3.12/site-packages:$PYTHONPATH"
```

**Ubuntu/Debian:**
```bash
sudo apt install fontforge python3-fontforge
```

**Windows:**
Download from [FontForge website](https://fontforge.org/en-US/downloads/)

## Running the command

```bash
# With default options
python3 generate-font.py

# With custom options
python3 generate-font.py --css-output dist/filename.css --font-output=otherfolder/font.woff2 --css-font-src=../otherfolder/font.woff2
```

### Options

- `--css-output` - CSS file output path (default: `dist/css/masked.css`)
- `--font-output` - Font file output path (default: `dist/fonts/masked.woff2`) 
- `--css-font-src` - Font URL to use in CSS @font-face src (default: `../fonts/masked.woff2`)
