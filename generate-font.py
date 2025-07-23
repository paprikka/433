import fontforge
import os
import argparse

def parse_arguments():
    parser = argparse.ArgumentParser(description='Generate a masked font where all characters appear as dots')
    parser.add_argument('--css-output', 
                       default='dist/css/433.css',
                       help='Output path for CSS file (default: dist/css/433.css)')
    parser.add_argument('--font-output', 
                       default='dist/fonts/433.woff2',
                       help='Output path for font file (default: dist/fonts/433.woff2)')
    parser.add_argument('--css-font-src', 
                       default='/fonts/433.woff2',
                       help='Font source URL to use in CSS @font-face (default: /fonts/433.woff2)')
    return parser.parse_args()

args = parse_arguments()

# Create a completely new font from scratch
font = fontforge.font()
font.fontname = "433"
font.familyname = "433"
font.fullname = "433 Regular"
font.weight = "Regular"
font.encoding = "UnicodeFull"

# Set standard font metrics
font.em = 1000
font.ascent = 800
font.descent = 200

# Add basic metadata
font.copyright = "Copyright (c) 2025 Rafal Pastuszak <hello@sonnet.io>"
font.appendSFNTName("English (US)", "Designer", "Rafal Pastuszak")
font.appendSFNTName("English (US)", "License", "MIT License")

# Create dot glyph template
dot_width = 600
dot_glyph = font.createChar(0x25CF, "blackcircle")
dot_glyph.width = dot_width
dot_glyph.clear()

# Draw a simple filled circle
pen = dot_glyph.glyphPen()
pen.moveTo((300, 200))
pen.curveTo((350, 200), (400, 250), (400, 300))
pen.curveTo((400, 350), (350, 400), (300, 400))
pen.curveTo((250, 400), (200, 350), (200, 300))
pen.curveTo((200, 250), (250, 200), (300, 200))
pen.closePath()
pen = None

print("Created dot template")

# Define whitespace characters that should preserve their spacing
whitespace_chars = {
    0x0020: 500,  # Space
    0x00A0: 500,  # Non-breaking space
    0x0009: 500,  # Tab
    0x000A: 0,    # Line feed
    0x000D: 0,    # Carriage return
    0x1680: 500,  # Ogham space mark
    0x2000: 500,  # En quad
    0x2001: 1000, # Em quad
    0x2002: 500,  # En space
    0x2003: 1000, # Em space
    0x2004: 333,  # Three-per-em space
    0x2005: 250,  # Four-per-em space
    0x2006: 167,  # Six-per-em space
    0x2007: 500,  # Figure space
    0x2008: 250,  # Punctuation space
    0x2009: 200,  # Thin space
    0x200A: 100,  # Hair space
    0x202F: 200,  # Narrow no-break space
    0x205F: 250,  # Medium mathematical space
    0x3000: 1000, # Ideographic space
}

# Create whitespace glyphs
for codepoint, width in whitespace_chars.items():
    glyph = font.createChar(codepoint)
    glyph.width = width
    # Leave empty (no drawing) for whitespace

print(f"Created {len(whitespace_chars)} whitespace glyphs")

# Create dot glyphs for all valid codepoints using FontForge's encoding
total_glyphs = 0
# Use Basic Multilingual Plane (0x0000-0xFFFF) which covers most common characters
for codepoint in range(0x21, 0xFFFE):  # Start from 0x21 to skip control chars, end before 0xFFFF
    # Skip if it's a whitespace character
    if codepoint in whitespace_chars:
        continue
        
    # Skip the dot glyph itself to avoid self-reference
    if codepoint == 0x25CF:
        continue
        
    # Create glyph that references the dot template
    try:
        glyph = font.createChar(codepoint)
        glyph.width = dot_width
        # Use addReference instead of drawing - much more efficient
        glyph.addReference(dot_glyph.glyphname)
        total_glyphs += 1
    except Exception:
        # Skip invalid codepoints
        pass

print(f"Created {total_glyphs} dot glyphs across Basic Multilingual Plane")

# Create output directories if they don't exist
font_dir = os.path.dirname(args.font_output)
css_dir = os.path.dirname(args.css_output)

if font_dir:
    os.makedirs(font_dir, exist_ok=True)
if css_dir:
    os.makedirs(css_dir, exist_ok=True)

# Generate WOFF2 font
font.generate(args.font_output)
print(f"Generated {args.font_output}")

# Generate CSS with @font-face declaration
css_content = f"""@font-face {{
  font-family: '433';
  src: url('{args.css_font_src}') format('woff2');
  font-weight: normal;
  font-style: normal;
  font-display: swap;
}}
"""

with open(args.css_output, "w") as f:
    f.write(css_content)

print(f"Generated {args.css_output}")

font.close()
print("Font generation complete!")

