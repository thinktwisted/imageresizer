#! python3
# imageResizer.py - resizes all images in a folder based on user input
# By John Van Fossen
# ThinkTwisted.com
#
# Images are resized in place: the original files are overwritten!

import argparse
import math
import sys
from pathlib import Path

from PIL import Image

IMAGE_SUFFIXES = {".png", ".jpg", ".jpeg"}
JPEG_SUFFIXES = {".jpg", ".jpeg"}
JPEG_QUALITY = 90


def parse_args(argv):
    parser = argparse.ArgumentParser(
        description="Resize every large image in a folder, overwriting the "
                    "original files.")
    parser.add_argument("directory", nargs="?", default=".",
                        help="folder to process (default: current directory)")
    parser.add_argument("-p", "--percent", type=float, metavar="PCT",
                        help="resize percentage, e.g. 50 (omit to be asked)")
    parser.add_argument("-m", "--min-size", type=float, default=1.0,
                        metavar="MB",
                        help="skip images under this many megabytes "
                             "(default: 1)")
    parser.add_argument("--no-gui", action="store_true",
                        help="prompt in the console instead of dialog boxes")
    return parser.parse_args(argv)


def alert(message, title, no_gui):
    """Show a dialog box, unless dialogs are disabled or unavailable."""
    if no_gui:
        return
    try:
        import pyautogui as gui
        gui.alert(message, title)
    except Exception:
        pass  # no display or no pyautogui; the console output is enough


def get_percent(no_gui):
    """Ask for a resize percentage greater than zero.

    Cancelling the dialog exits cleanly; bad input is re-asked.
    Falls back to console input when dialogs are unavailable.
    """
    while True:
        if no_gui:
            try:
                raw = input("What is the resize percent? ")
            except EOFError:
                sys.exit("No input available; pass --percent.")
        else:
            try:
                import pyautogui as gui
                raw = gui.prompt("What is the resize percent?")
            except ImportError:
                no_gui = True
                continue
            except Exception:
                no_gui = True  # dialogs need a display; use the console
                continue
            if raw is None:  # the user pressed Cancel
                sys.exit(0)
        try:
            percent = float(raw)
        except ValueError:
            message = "Please enter a number, e.g. 50."
            print(message)
            alert(message, "imageresizer", no_gui)
            continue
        if percent > 0 and math.isfinite(percent):
            return percent
        message = "Please enter a percentage greater than 0."
        print(message)
        alert(message, "imageresizer", no_gui)


def process_file(path, scale):
    """Resize one image by scale and save over the original."""
    with Image.open(path) as im:
        width, height = im.size
        size = (max(1, int(width * scale)), max(1, int(height * scale)))
        resized = im.resize(size, Image.LANCZOS)
    params = {}
    if path.suffix.lower() in JPEG_SUFFIXES:
        params["quality"] = JPEG_QUALITY
    resized.save(path, **params)


def main(argv=None):
    args = parse_args(sys.argv[1:] if argv is None else argv)
    folder = Path(args.directory)
    if not folder.is_dir():
        sys.exit(f"error: '{args.directory}' is not a directory")
    if args.min_size < 0:
        sys.exit("error: --min-size must not be negative")

    if args.percent is not None:
        if args.percent <= 0 or not math.isfinite(args.percent):
            sys.exit("error: --percent must be greater than 0")
        percent = args.percent
    else:
        percent = get_percent(args.no_gui)
    scale = percent / 100.0
    min_bytes = int(args.min_size * 1024 * 1024)

    done = failed = 0
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.suffix.lower() not in IMAGE_SUFFIXES:
            continue
        if path.stat().st_size < min_bytes:
            continue
        print(f"Resizing {path.name}...")
        try:
            process_file(path, scale)
            done += 1
        except Exception as exc:
            failed += 1
            print(f"  FAILED {path.name}: {exc}", file=sys.stderr)

    message = f"{done} images resized."
    if failed:
        message += f" {failed} failed."
    print(message)
    alert(message, "FINISHED!", args.no_gui)


if __name__ == "__main__":
    main()
