# imageresizer

A simple Python image resizer. Bulk-resizes every large image in a folder down
to a percentage you pick — handy for shrinking a directory of multi-megabyte
photos in one pass.

## How it works

1. It scans the files in the folder you give it (default: the current
   directory).
2. Files are skipped unless their extension is `.png`, `.jpg`, or `.jpeg`,
   in any capitalization.
3. Images smaller than 1 MB by default are skipped — they are assumed to be
   small enough already (`-m` changes the threshold).
4. Each remaining image is resized with a high-quality Lanczos filter and
   **saved over the original file** (JPEGs are saved at quality 90).
5. When finished, it prints a summary (resized count plus any failures) and,
   if dialogs are available, shows a "FINISHED!" alert.

> **Warning:** this tool overwrites your originals and there is no undo.
> Copy the folder somewhere safe (or keep it under backup/version control)
> before running it.

## Requirements

- Python 3 with [Pillow](https://python-pillow.org/)
- Optionally [PyAutoGUI](https://pyautogui.readthedocs.io/) for the dialog
  boxes; without it (or with `--no-gui`) the tool prompts in the console

```
pip install -r requirements.txt
```

## Usage

```
python imageResizer.py [directory] [-p PERCENT] [-m MB] [--no-gui]
```

| Argument | Meaning |
| --- | --- |
| `directory` | Folder to process. Default: current folder. |
| `-p, --percent` | Resize percentage, e.g. `50` for half size. Omit to be asked in a dialog (or on the console). |
| `-m, --min-size` | Skip images under this many MB. Default: `1`. |
| `--no-gui` | Ask in the console instead of showing dialog boxes. |

Examples:

```
python imageResizer.py                     # ask for percent, process "."
python imageResizer.py C:\Photos -p 50     # halve every large image in C:\Photos
python imageResizer.py . -p 75 -m 2        # 75%, only files 2 MB or larger
```

Pressing Cancel in the percent dialog exits without touching any files.
A single unreadable or corrupt image is reported as a failure; the rest of
the batch still gets processed.

## Notes

- A percentage over 100 enlarges images.
- Re-saving JPEGs applies another round of lossy compression (generation
  loss), so resize from your best originals when you can.
- Subfolders are not scanned; only the files directly inside the given
  directory are processed.

## License

GPL-3.0 — see [LICENSE](LICENSE).

By John Van Fossen · ThinkTwisted.com
