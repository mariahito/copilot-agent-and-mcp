#!/usr/bin/env python3
# generated-by-copilot: Resize images into large, medium, small, and thumbnail variants using Pillow.

import argparse
import sys
from pathlib import Path

try:
    from PIL import Image
except ImportError:
    sys.exit("Pillow is required. Install it with: pip install Pillow")

SUPPORTED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp"}

DEFAULT_SIZES = {
    "large": 1920,
    "medium": 960,
    "small": 480,
    "thumbnail": 150,
}


def parse_sizes(sizes_arg: str) -> dict[str, int]:
    # generated-by-copilot: Parse comma-separated "name:pixels" pairs into a dict.
    result: dict[str, int] = {}
    for token in sizes_arg.split(","):
        token = token.strip()
        if not token:
            continue
        if ":" not in token:
            sys.exit(f"Invalid size specification '{token}'. Expected format: name:pixels")
        name, _, px = token.partition(":")
        name = name.strip()
        if not name:
            sys.exit(f"Size name is empty in '{token}'.")
        try:
            pixels = int(px.strip())
        except ValueError:
            sys.exit(f"Invalid pixel value in '{token}'. Must be an integer.")
        if pixels <= 0:
            sys.exit(f"Pixel value must be positive, got {pixels} in '{token}'.")
        result[name] = pixels
    if not result:
        sys.exit("--sizes produced an empty mapping. Check your input.")
    return result


def collect_images(input_path: Path) -> list[Path]:
    # generated-by-copilot: Collect all supported image files from a file or directory path.
    if input_path.is_file():
        if input_path.suffix.lower() not in SUPPORTED_EXTENSIONS:
            sys.exit(
                f"File '{input_path}' has an unsupported extension. "
                f"Supported: {', '.join(sorted(SUPPORTED_EXTENSIONS))}"
            )
        return [input_path]

    if input_path.is_dir():
        images = [
            p for p in sorted(input_path.iterdir())
            if p.is_file() and p.suffix.lower() in SUPPORTED_EXTENSIONS
        ]
        if not images:
            sys.exit(f"No supported images found in directory '{input_path}'.")
        return images

    sys.exit(f"Input path '{input_path}' does not exist.")


def resize_image(src: Path, dest: Path, max_px: int) -> None:
    # generated-by-copilot: Resize a single image so its longest edge is at most max_px, preserving aspect ratio.
    with Image.open(src) as img:
        original_mode = img.mode
        width, height = img.size
        longest = max(width, height)

        if longest <= max_px:
            # generated-by-copilot: Image is already within target size; copy as-is to preserve quality.
            resized = img.copy()
        else:
            scale = max_px / longest
            new_width = max(1, round(width * scale))
            new_height = max(1, round(height * scale))
            resized = img.resize((new_width, new_height), Image.LANCZOS)

        # generated-by-copilot: Convert palette/transparency modes for JPEG compatibility.
        save_mode = original_mode
        suffix = dest.suffix.lower()
        if suffix in {".jpg", ".jpeg"} and original_mode in {"RGBA", "P", "LA"}:
            resized = resized.convert("RGB")
            save_mode = "RGB"

        dest.parent.mkdir(parents=True, exist_ok=True)
        resized.save(dest)


def process(
    input_path: Path,
    output_dir: Path,
    sizes: dict[str, int],
    overwrite: bool,
) -> None:
    # generated-by-copilot: Process all collected images and write resized variants to output_dir.
    images = collect_images(input_path)
    skipped = 0
    written = 0

    for src in images:
        for variant_name, max_px in sizes.items():
            dest = output_dir / variant_name / src.name
            if dest.exists() and not overwrite:
                print(f"  [skip]  {dest} (use --overwrite to replace)")
                skipped += 1
                continue
            print(f"  [write] {dest}  ({max_px}px max)")
            resize_image(src, dest, max_px)
            written += 1

    print(f"\nDone. {written} file(s) written, {skipped} skipped.")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Resize images into multiple size variants using Pillow.",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Resize a single file
  python resize_images.py --input photo.jpg

  # Resize all images in a directory
  python resize_images.py --input photos/

  # Custom output directory
  python resize_images.py --input photos/ --output public/assets/resized

  # Custom sizes
  python resize_images.py --input photos/ --sizes "large:2560,medium:1280,small:640,thumbnail:200"

  # Overwrite existing output files
  python resize_images.py --input photos/ --overwrite
""",
    )
    parser.add_argument(
        "--input",
        required=True,
        metavar="PATH",
        help="Path to an image file or a directory of images.",
    )
    parser.add_argument(
        "--output",
        default="images/resized",
        metavar="DIR",
        help="Output directory for resized images (default: images/resized).",
    )
    parser.add_argument(
        "--sizes",
        default=None,
        metavar="SIZES",
        help=(
            "Comma-separated name:pixels pairs, e.g. 'large:1920,medium:960,small:480,thumbnail:150'. "
            "Defaults to: large:1920, medium:960, small:480, thumbnail:150."
        ),
    )
    parser.add_argument(
        "--overwrite",
        action="store_true",
        help="Overwrite existing output files. By default, existing files are skipped.",
    )

    args = parser.parse_args()

    sizes = parse_sizes(args.sizes) if args.sizes else DEFAULT_SIZES
    input_path = Path(args.input)
    output_dir = Path(args.output)

    print(f"Input:   {input_path}")
    print(f"Output:  {output_dir}")
    print(f"Sizes:   {', '.join(f'{k}:{v}px' for k, v in sizes.items())}")
    print(f"Overwrite: {args.overwrite}")
    print()

    process(input_path, output_dir, sizes, args.overwrite)


if __name__ == "__main__":
    main()
