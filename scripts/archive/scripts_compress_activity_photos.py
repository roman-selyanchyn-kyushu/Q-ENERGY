#!/usr/bin/env python3
"""
Compress and resize activity photos for the web.

- Scans assets/photos/activities/*/  for any JPG/PNG/HEIC files
- Resizes to max 1200px wide (keeps aspect ratio)
- Saves as JPG at quality 82 — typically 80–200 KB per photo
- Renames output to 01.jpg, 02.jpg … in alphabetical order
- Originals are preserved in an _originals/ subfolder

Run from project root:
    python3 scripts_compress_activity_photos.py

Requires Pillow:
    pip install Pillow
"""

from pathlib import Path
from PIL import Image
import shutil

BASE        = Path(__file__).parent
PHOTOS_DIR  = BASE / "assets" / "photos" / "activities"
MAX_WIDTH   = 1200
QUALITY     = 82
EXTENSIONS  = {".jpg", ".jpeg", ".png", ".heic", ".webp", ".tiff", ".tif"}


def compress_folder(folder: Path):
    # Collect source images (skip already-processed 01.jpg etc. if re-running)
    originals_dir = folder / "_originals"

    # Find all image files, excluding _originals subfolder
    sources = sorted([
        f for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in EXTENSIONS
    ])

    if not sources:
        print(f"  {folder.name}/  — no images found, skipping")
        return

    # Move originals to _originals/ for safekeeping
    originals_dir.mkdir(exist_ok=True)
    for src in sources:
        dest = originals_dir / src.name
        if not dest.exists():
            shutil.copy2(src, dest)
            print(f"    backed up {src.name} → _originals/")

    # Process each image
    print(f"  {folder.name}/  — {len(sources)} image(s)")
    for i, src in enumerate(sources, start=1):
        out_name = f"{i:02d}.jpg"
        out_path = folder / out_name

        try:
            img = Image.open(src).convert("RGB")
            w, h = img.size

            # Resize if wider than MAX_WIDTH
            if w > MAX_WIDTH:
                new_h = int(h * MAX_WIDTH / w)
                img = img.resize((MAX_WIDTH, new_h), Image.LANCZOS)
                resized = f"{w}×{h} → {MAX_WIDTH}×{new_h}"
            else:
                resized = f"{w}×{h} (no resize needed)"

            img.save(out_path, "JPEG", quality=QUALITY, optimize=True)
            kb = out_path.stat().st_size // 1024
            print(f"    {src.name} → {out_name}  [{resized}]  {kb} KB")

            # Remove original from folder root (it's safe in _originals/)
            if src != out_path:
                src.unlink()

        except Exception as e:
            print(f"    ERROR processing {src.name}: {e}")


def main():
    if not PHOTOS_DIR.exists():
        print(f"Directory not found: {PHOTOS_DIR}")
        return

    folders = [f for f in sorted(PHOTOS_DIR.iterdir()) if f.is_dir() and not f.name.startswith("_")]
    if not folders:
        print("No activity subfolders found.")
        return

    print(f"Compressing activity photos in {PHOTOS_DIR}\n")
    for folder in folders:
        compress_folder(folder)

    print("\nDone. Originals saved in each folder's _originals/ subfolder.")


if __name__ == "__main__":
    main()
