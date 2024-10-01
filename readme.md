# SubShifter v2

SubShifter v2 is a simple program for shifting subtitles in .srt format. It allows the user to shift subtitles by a specified number of seconds.

## Requirements

- Python 3.x
- `pysrt` library
- `tkinter` library

## Usage

### From Command Line

1. Run the program from the command line, providing the .srt file as an argument:
   ```bash
   python main.py path/to/your/subtitles.srt
   ```
2. Enter the number of seconds you want to shift the subtitles in the dialog box.

### Drag and Drop

The program has also been compiled into an executable .exe file. You can drag and drop the subtitle file onto the program icon for quick shifting.

After selecting the shift time, multiple files will be generated, each shifted by one second.

## Example

To shift subtitles forward by 5 seconds:

1. Run the program.
2. Enter `5` in the dialog box.

## License

This project is licensed under the MIT License. You can use, modify, and distribute it according to the terms of this license.
