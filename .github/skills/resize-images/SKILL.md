---
name: resize-images
description: 'Resize images into multiple size variants (large, medium, small, thumbnail) using Python and Pillow. Use when resizing images, generating image variants, batch processing image files, or creating responsive image sets. Supports .png, .jpg, .jpeg, .webp. Preserves aspect ratio. Accepts a single file or a full directory as input.'
argument-hint: 'path to an image file or directory of images'
---

# Resize Images

Generates **large**, **medium**, **small**, and **thumbnail** variants of images while preserving aspect ratio. Processes a single file or an entire directory.

## When to Use

- Resizing a single image or a batch of images
- Generating responsive image sets for web projects
- Creating thumbnail previews from originals
- Converting images to multiple standard sizes in one pass

## Supported Formats

`.png`, `.jpg`, `.jpeg`, `.webp`

## Default Sizes

| Variant    | Max dimension (px) |
|------------|--------------------|
| large      | 1920               |
| medium     | 960                |
| small      | 480                |
| thumbnail  | 150                |

Each image is scaled so that its longest edge fits within the configured max dimension; the other dimension is calculated to preserve the original aspect ratio.

## Procedure

1. Ensure Python 3 and Pillow are available:
   ```bash
   pip install Pillow
   ```
2. Run [resize_images.py](./resize_images.py) with the appropriate flags (see **Usage** below).
3. Resized files are saved to the output directory (default: `images/resized/`), organised into sub-folders per variant: `large/`, `medium/`, `small/`, `thumbnail/`.
4. Original filenames are preserved; the variant name is **not** appended to the filename — the sub-folder conveys the size.

## Usage

### Resize a single file
```bash
python .github/skills/resize-images/resize_images.py --input path/to/photo.jpg
```

### Resize all images in a directory
```bash
python .github/skills/resize-images/resize_images.py --input path/to/photos/
```

### Custom output directory
```bash
python .github/skills/resize-images/resize_images.py --input path/to/photos/ --output public/assets/resized
```

### Custom sizes (comma-separated `name:pixels` pairs)
```bash
python .github/skills/resize-images/resize_images.py --input path/to/photos/ --sizes "large:2560,medium:1280,small:640,thumbnail:200"
```

### Overwrite existing output files
```bash
python .github/skills/resize-images/resize_images.py --input path/to/photos/ --overwrite
```

## Flags

| Flag          | Default           | Description                                                                 |
|---------------|-------------------|-----------------------------------------------------------------------------|
| `--input`     | *(required)*      | Path to an image file or a directory of images.                             |
| `--output`    | `images/resized`  | Directory where variant sub-folders will be created.                        |
| `--sizes`     | see table above   | Comma-separated `name:max_px` pairs, e.g. `large:1920,thumbnail:150`.      |
| `--overwrite` | `False`           | If set, existing output files are replaced. Otherwise they are skipped.     |

## Output Structure

```
images/resized/
├── large/
│   └── photo.jpg
├── medium/
│   └── photo.jpg
├── small/
│   └── photo.jpg
└── thumbnail/
    └── photo.jpg
```
