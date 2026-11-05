# imageresizer

A simple Python image resizer. Bulk-resizes every large image in a folder down
to a percentage you pick — handy for shrinking a directory of multi-megabyte
photos in one pass.

## How it works

1. On launch, a dialog asks for a **resize percentage** (e.g. `50` for half
   size).
2. It scans every file in the **current working directory** — the folder you
   run the script from, not the folder the script lives in.
3. Files are skipped unless their name ends in `.png`, `.jpg`, `.PNG`, `.JPG`,
   `.jpeg`, or `.JPEG`.
4. Images smaller than about **1 MB** are skipped — they are assumed to be
   small enough already.
5. Each remaining image is resized by the percentage and
   **saved over the original file**.
6. When finished, it prints a count to the console and shows a "FINISHED!"
   alert dialog.

> **Warning:** this tool overwrites your originals and there is no undo.
> Copy the folder somewhere safe (or keep it under backup/version control)
> before running it.

## Requirements

- Python 3
- [Pillow](https://python-pillow.org/) — image processing
- [PyAutoGUI](https://pyautogui.readthedocs.io/) — the prompt/alert dialogs

```
pip install pillow pyautogui
```

## Usage

```
cd path\to\photos
python imageResizer.py
```

Type the resize percentage into the dialog and press OK. Each image is
reported in the terminal as it is processed; an alert box shows the total
count when done.

## Notes and limitations

- Enter a whole number below 100 to shrink images. Cancel, empty input, or
  non-numeric input will crash the script — there is no validation.
- A percentage above 100 will enlarge the image instead.
- Re-saving JPEGs applies another round of lossy compression (generation
  loss), so try to resize from your best originals.
- Subfolders are not scanned; only the flat directory listing is processed.
- The size threshold and extension checks are hardcoded near the top of the
  loop in `imageResizer.py` — edit them there if you want different values.

## License

GPL-3.0 — see [LICENSE](LICENSE).

By John Van Fossen · ThinkTwisted.com
