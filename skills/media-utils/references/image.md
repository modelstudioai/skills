# Image processing

Use `python3 scripts/media_utils.py` below relative to the skill directory.

## Inspect and convert

```bash
python3 scripts/media_utils.py probe photo.heic
python3 scripts/media_utils.py image convert photo.webp photo.png
```

Supported output extensions are `.png`, `.jpg`/`.jpeg`, `.bmp`, and `.tif`/`.tiff`.
WebP output is also available when this scoped check passes:

```bash
python3 scripts/media_utils.py doctor --for-operation image-webp --install-plan
```

It requires an ffmpeg build with `libwebp`. Image commands intentionally strip metadata
and write one frame.

## Resize and thumbnail

Preserve aspect ratio when only one dimension is supplied:

```bash
python3 scripts/media_utils.py image resize photo.png resized.png --width 1200
python3 scripts/media_utils.py image resize photo.png resized.png --height 800
```

When both dimensions are supplied, the image fits inside the requested box. Pass
`--stretch` only when distortion is explicitly wanted.

Create an exact-size padded thumbnail:

```bash
python3 scripts/media_utils.py image thumbnail photo.png thumb.jpg \
  --width 640 --height 360 --background black
```

## Crop, rotate, and flip

```bash
python3 scripts/media_utils.py image crop photo.png crop.png \
  --width 800 --height 800 --x 120 --y 40
python3 scripts/media_utils.py image rotate photo.png rotated.png --degrees 90
python3 scripts/media_utils.py image flip photo.png mirrored.png --direction horizontal
```

Probe the output to verify dimensions and pixel format. Use PNG or WebP when transparency
must be retained; JPEG cannot carry Alpha.

## Scope boundary

This deterministic tier does not perform semantic object removal, AI upscaling, OCR scoring,
or arbitrary subject matting. Do not simulate transparency by claiming a generative image
editor produced a reliable Alpha mask.
