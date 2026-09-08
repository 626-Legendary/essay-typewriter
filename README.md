# Essay Typewriter

A lightweight console-based automation tool that simulates realistic human typing. It reads the contents of a text file and "types" them into whatever window currently has focus—whether that’s Microsoft Word, a browser-based text editor, or any other input field. The typing rhythm mimics a real person: variable speed, brief pauses at punctuation and spaces, and occasional typos that are instinctively corrected.

![App Demo](./images/demo.gif)

**Why this tool exists**  
Many universities now require students to submit essays through platforms like Grammarly, which monitor clipboard activity and keystroke patterns to detect AI-generated content. As a result, students with longer papers are forced to manually retype their own drafts—an unnecessarily time-consuming and error-prone process. This tool was created to solve that problem: it automates the typing of any pre-written text while preserving a natural, human-like input pattern. You can adjust typing speed, enable or disable “thinking” pauses, and even simulate realistic typos. The result? Your essay appears to have been typed by hand over the course of hours—giving you back your time without raising red flags.

---

## Features

- **Human-like typing rhythm** — speed varies per character, with natural pauses after spaces and punctuation; occasional typo simulation (neighboring-key slips that are immediately backspaced and corrected) adds authenticity.
- **Adjustable typing speed** — choose from presets like *College Student*, *High School Student*, or *International Student*, or define a custom words-per-minute (WPM) value.
- **Configurable thinking pauses** — toggle on/off and customize the minimum and maximum pause duration.
- **Typo simulation toggle** — enable or disable realistic mistake-and-correction behavior.
- **Persistent settings** — all preferences are saved to `config.ini` and reloaded on startup.
- **Portable data files** — `content.txt` and `config.ini` are always read from and written to the folder containing the executable, even when bundled as a single `.exe` via PyInstaller—making them easy to locate and edit.
- **Emergency stop** — press the `ESC` key at any time to halt typing immediately.

---

## Requirements

- Python 3.8 or higher
- [`keyboard`](https://pypi.org/project/keyboard/)
- [`pyautogui`](https://pypi.org/project/pyautogui/)

Install dependencies with:

```bash
pip install keyboard pyautogui
```

> **Note:** On some operating systems, the `keyboard` library may require administrator/root privileges to register the global `ESC` hotkey.

---

## Usage

1. Run the script:
   ```bash
   python essay_typewriter.py
   ```

2. On first launch, you will be prompted to create default `content.txt` and `config.ini` files in the program directory.

3. Paste the text you want typed into `content.txt` and save.

4. From the main menu, adjust settings as desired (typing speed, thinking pauses, typo simulation), or proceed with the defaults.

5. Select **Start Typing**. A 5‑second countdown will begin—use this time to switch to your target window and click into the input field so it has focus. Typing starts automatically once the countdown ends.

6. Press `ESC` at any time to stop the process.

---

## Building a Standalone Executable

You can package the project into a single `.exe` file using [PyInstaller](https://pyinstaller.org/):

```bash
python -m PyInstaller --onefile --clean --name=EssayTyper --icon=typewriter.ico --version-file=version_info.txt essay_typewriter.py
```

After building, `content.txt` and `config.ini` will be created and accessed alongside `EssayTyper.exe` (not in a temporary folder), ensuring your settings and content persist between runs and remain easy to modify manually.

---

## Configuration Reference (`config.ini`)

| Key | Values | Description |
|-----|--------|-------------|
| `speed` | `COLLEGE_STUDENT`, `HIGH_SCHOOL_STUDENT`, `INTERNATIONAL_STUDENT`, `CUSTOM` | Typing speed preset |
| `custom_wpm` | number | Words per minute used when `speed = CUSTOM` |
| `real_thinking` | `true` / `false` | Whether to insert brief pauses at spaces and punctuation |
| `min_thinking_time` / `max_thinking_time` | seconds | Range for thinking pauses |
| `real_typing` | `true` / `false` | Whether to simulate realistic typos |

All settings can also be adjusted via the in-app **Settings** menu.

---

## Disclaimer

This tool is designed for legitimate personal productivity and accessibility purposes—for example, re‑typing your own drafted content into a document. It is your responsibility to use this software in accordance with the terms of service of any application or platform you interact with, as well as to ensure the content being typed complies with applicable policies.

---

## Contributing

Issues and pull requests are welcome. Feel free to open an issue or reach out directly with questions, bug reports, or feature suggestions.

---

## License

This project is licensed under the [MIT License](LICENSE).

---

## Author

**Zexiang Zhang**  
GitHub: [https://github.com/626-Legendary/](https://github.com/626-Legendary/)

---