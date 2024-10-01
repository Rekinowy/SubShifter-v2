import sys
import pysrt
import tkinter as tk
from tkinter import simpledialog, messagebox
import re


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

def main():
    # Check if file exists
    if len(sys.argv) > 1:
        filename = sys.argv[1]

        if not filename.endswith('.srt'):
            messagebox.showerror(
                "Błąd", "Dostarczony plik nie jest w formacie .srt")
            return

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
        messagebox.showerror("Błąd", "Nie podano pliku .srt")

if __name__ == "__main__":
    main()
