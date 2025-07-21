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
python3 generate-font.py
```

The script will:
- Generate `../src/assets/fonts/masked.woff2`
- Generate `../src/masked-font.css` with @font-face declaration