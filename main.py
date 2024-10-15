import sys
import os
import shutil
import re
import zipfile
import pysrt
import tkinter as tk
from tkinter import simpledialog, messagebox
from send2trash import send2trash


def main():
    # Check if file exists
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        if not filename.endswith(('.srt', '.zip')):
            messagebox.showerror(
                "Błąd", "Dostarczony plik nie jest w formacie .srt lub .zip")
            return

        # Checking if rchive and extracting
        if filename.endswith('.zip'):
            filename = extract_srt_from_archive(filename)

        # Create dialog box
        root = tk.Tk()
        root.withdraw()  # Hide main window

        try:
            # Ask the user to enter shift time
            shift_time = simpledialog.askinteger(
                title="SubShifter v2",
                prompt="O ile sekund przesunąć napisy?",
            )
            if shift_time is not None:
                shift_subs(filename, shift_time)
        except Exception as e:
            messagebox.showerror("Błąd", f"Wystąpił błąd: {str(e)}")

    else:
        messagebox.showerror("Błąd", "Nie podano pliku")


def shift_subs(file, seconds=1):
    try:
        # Load subtitles from file
        subs = pysrt.open(file)

        # Extract current shift from filename if present
        match = re.search(r'\[([-+]?\d+)s\]', file)
        current_shift = int(match.group(1)) if match else 0

        # Shift the subtitles
        for i in range(abs(seconds)):
            shift_amount = 1 if seconds > 0 else -1
            total_shift = current_shift + shift_amount * (i + 1)
            subs.shift(seconds=shift_amount)
            if total_shift == 0:
                continue

            # Save new file with updated shift in name
            sign = '+' if total_shift > 0 else ''
            new_name = re.sub(r'\s*\[([-+]?\d+)s\]', '', file).replace(
                '.srt', f' [{sign}{total_shift}s].srt')
            subs.save(new_name, encoding='utf8')
    except Exception as e:
        messagebox.showerror(
            "Błąd", f"Nie udało się przetworzyć pliku: {str(e)}")


def extract_srt_from_archive(archive_path):
    with zipfile.ZipFile(archive_path, 'r') as zip_ref:
        # Extracting to temporary location
        zip_ref.extractall('temp_dir')

    # Searching for .srt file
    srt_file_path = None
    for file in os.listdir('temp_dir'):
        if file.endswith('.srt'):
            srt_file_path = os.path.join('temp_dir', file)
            break

    if not srt_file_path:
        shutil.rmtree('temp_dir')  # Deleting temp_dir
        messagebox.showerror("Błąd", "Nie znaleziono pliku .srt w archiwum")
        sys.exit(1)

    # Cleanup
    new_srt_path = cleanup(archive_path, srt_file_path)
    return new_srt_path


def cleanup(archive_path, srt_file_path):
    # Moving .srt file to original location
    new_srt_path = os.path.join(os.path.dirname(
        archive_path), os.path.basename(srt_file_path))
    shutil.move(srt_file_path, new_srt_path)

    # Deleting temporary files and archive
    send2trash(archive_path)
    shutil.rmtree('temp_dir')

    return new_srt_path


if __name__ == "__main__":
    main()
