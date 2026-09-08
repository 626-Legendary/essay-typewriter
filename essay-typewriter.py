#   ______                       _______                             _ _
#  |  ____|                     |__   __|                           (_) |
#  | |__   ___ ___  __ _ _   _     | |_   _ _ __   _____      ___ __ _| |_ ___ _ __
#  |  __| / __/ __|/ _` | | | |    | | | | | '_ \ / _ \ \ /\ / / '__| | __/ _ \ '__|
#  | |____\__ \__ \ (_| | |_| |    | | |_| | |_) |  __/\ V  V /| |  | | ||  __/ |
#  |______|___/___/\__,_|\__, |    |_|\__, | .__/ \___| \_/\_/ |_|  |_|\__\___|_|
#                         __/ |        __/ | |
#                        |___/        |___/|_|
#
# GitHub: https://github.com/626-Legendary/

import configparser
import random
import sys
import time
from pathlib import Path

import keyboard
import pyautogui

from typing_engine import *

def get_base_dir() -> Path:
    """Return the folder where content.txt / config.ini should live."""
    if getattr(sys, "frozen", False):
        return Path(sys.executable).resolve().parent
    return Path(__file__).resolve().parent


BASE_DIR = get_base_dir()
CONTENT_PATH = BASE_DIR / "content.txt"
CONFIG_PATH = BASE_DIR / "config.ini"

# ---------------------------------------------------------------------------
# Console Styling
# ---------------------------------------------------------------------------


class Color:
    RESET = "\033[0m"
    BOLD = "\033[1m"
    DIM = "\033[2m"
    RED = "\033[31m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"
    CYAN = "\033[36m"
    MAGENTA = "\033[35m"


def clear_screen() -> None:
    """Clear the terminal (works in most Windows/macOS/Linux terminals)."""
    print("\033[2J\033[H", end="")


def status_label(is_on: bool) -> str:
    """Colored On/Off badge: green for On, red for Off."""
    if is_on:
        return f"{Color.GREEN}{Color.BOLD}On{Color.RESET}"
    return f"{Color.RED}{Color.BOLD}Off{Color.RESET}"


def print_title(title: str, width: int = 45) -> None:
    bar = "─" * width
    print(f"{Color.CYAN}{Color.BOLD}╭{bar}╮{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}│{title.center(width)}│{Color.RESET}")
    print(f"{Color.CYAN}{Color.BOLD}╰{bar}╯{Color.RESET}\n")


def option_line(key: str, label: str) -> str:
    return f"  {Color.YELLOW}{Color.BOLD}[{key}]{Color.RESET} {label}"


def pause() -> None:
    input(f"{Color.DIM}Press Enter to continue...{Color.RESET}")


is_running = True

# ---------------------------------------------------------------------------
# Typing speed presets
# ---------------------------------------------------------------------------

SPEED_PRESET_WPM = {
    "COLLEGE_STUDENT": 50,
    "HIGH_SCHOOL_STUDENT": 45,
    "INTERNATIONAL_STUDENT": 22,
} 

# Display order for the settings menu: College Student is the default.
SPEED_ORDER = ["COLLEGE_STUDENT", "HIGH_SCHOOL_STUDENT", "INTERNATIONAL_STUDENT", "CUSTOM"]

SPEED_NAMES = {
    "COLLEGE_STUDENT": "College Student",
    "HIGH_SCHOOL_STUDENT": "High School Student",
    "INTERNATIONAL_STUDENT": "International Student",
    "CUSTOM": "Custom",
}

DEFAULT_CUSTOM_WPM = 40

# Runtime settings
TYPING_SPEED_MODE = "COLLEGE_STUDENT"
CUSTOM_WPM = DEFAULT_CUSTOM_WPM
min_thinking_time = 0.5
max_thinking_time = 5.0
REAL_THINKING = True
REAL_TYPING = True  # whether to simulate realistic typos

DEFAULT_MIN_THINKING = 0.5
DEFAULT_MAX_THINKING = 5.0

def wpm_to_interval(wpm: float) -> float:
    """Convert words-per-minute into a seconds-per-character base interval."""
    # 5 chars = 1 word
    # print("wpm:", wpm) 
    factor = 1.5
    return 60/(wpm * 5 * factor)


def current_wpm() -> float:
    if TYPING_SPEED_MODE == "CUSTOM":
        return CUSTOM_WPM
    return SPEED_PRESET_WPM[TYPING_SPEED_MODE]


def speed_label(mode: str, custom_wpm: float = None) -> str:
    if mode == "CUSTOM":
        wpm = custom_wpm if custom_wpm is not None else CUSTOM_WPM
        return f"Custom (~{wpm:g} WPM)"
    return f"{SPEED_NAMES[mode]} (~{SPEED_PRESET_WPM[mode]} WPM)"


# ---------------------------------------------------------------------------
# Config handling
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "Typing": {
        "speed": "COLLEGE_STUDENT",
        "custom_wpm": str(DEFAULT_CUSTOM_WPM),
        "real_thinking": "true",
        "min_thinking_time": str(DEFAULT_MIN_THINKING),
        "max_thinking_time": str(DEFAULT_MAX_THINKING),
        "real_typing": "true",
    }
}


def files_exist() -> bool:
    """Check whether both content.txt and config.ini are present."""
    return CONTENT_PATH.exists() and CONFIG_PATH.exists()


def write_default_files() -> None:
    """Create an empty content.txt and a default config.ini."""
    if not CONTENT_PATH.exists():
        CONTENT_PATH.write_text("", encoding="utf-8")

    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def load_config() -> configparser.ConfigParser:
    """Load config.ini, falling back to defaults for any missing keys."""
    config = configparser.ConfigParser()
    config.read_dict(DEFAULT_CONFIG)  # defaults first
    if CONFIG_PATH.exists():
        config.read(CONFIG_PATH, encoding="utf-8")
    return config


def save_config(config: configparser.ConfigParser) -> None:
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        config.write(f)


def apply_config_to_runtime(config: configparser.ConfigParser) -> None:
    """Push values from config.ini into the runtime globals used by typing."""
    global TYPING_SPEED_MODE, CUSTOM_WPM, REAL_THINKING, REAL_TYPING
    global min_thinking_time, max_thinking_time

    speed_name = config.get("Typing", "speed", fallback="COLLEGE_STUDENT")
    TYPING_SPEED_MODE = speed_name if speed_name in SPEED_ORDER else "COLLEGE_STUDENT"
    CUSTOM_WPM = config.getfloat("Typing", "custom_wpm", fallback=DEFAULT_CUSTOM_WPM)

    REAL_THINKING = config.getboolean("Typing", "real_thinking", fallback=True)
    REAL_TYPING = config.getboolean("Typing", "real_typing", fallback=True)

    if REAL_THINKING:
        min_thinking_time = config.getfloat("Typing", "min_thinking_time", fallback=DEFAULT_MIN_THINKING)
        max_thinking_time = config.getfloat("Typing", "max_thinking_time", fallback=DEFAULT_MAX_THINKING)
    else:
        min_thinking_time = 0.0
        max_thinking_time = 0.0


# ---------------------------------------------------------------------------
# First-run setup
# ---------------------------------------------------------------------------

def ensure_setup() -> bool:
    """
    If content.txt and config.ini already exist, skip setup silently.
    Otherwise, ask the user for permission to create default files.
    Returns False if the user declines (program should exit).
    """
    if files_exist():
        return True

    show_menu()
    print(f"{Color.YELLOW}[Setup]{Color.RESET} content.txt / config.ini not found in:\n  {Color.CYAN}{BASE_DIR}{Color.RESET}")
    answer = input("Create default content.txt and config.ini here? (Y/N): ").strip().lower()
    if answer == "y":
        write_default_files()
        print(f"{Color.GREEN}[+] Default files created at {BASE_DIR}{Color.RESET}\n")
        return True

    print(f"{Color.RED}[-] Setup declined. Exiting program.{Color.RESET}")
    return False


# ---------------------------------------------------------------------------
# Menu / UI
# ---------------------------------------------------------------------------

def show_menu():
    clear_screen()
    print_title("ESSAY TYPEWRITER")
    print(option_line("1", "Instructions"))
    print(option_line("2", "Start Typing"))
    print(option_line("3", "Settings"))
    print(option_line("4", "About"))
    print(option_line("Q", "Exit"))
    print()


def show_instructions():
    clear_screen()
    print_title("Instructions")
    print(f"""
{Color.BOLD}1.{Color.RESET} Copy the text you want Essay Typewriter to type and paste it into
{Color.CYAN}content.txt{Color.RESET}, then save the file.
{Color.BOLD}2.{Color.RESET} Adjust the settings if you'd like (or just use the defaults).
{Color.BOLD}3.{Color.RESET} Choose option {Color.YELLOW}[2] Start Typing{Color.RESET}. You'll have {Color.RED}5 seconds{Color.RESET} to switch
to the target window (e.g. Word) and click into it so it has focus.
Typing will begin automatically once the countdown ends.
{Color.BOLD}4.{Color.RESET} If anything goes wrong, press {Color.RED}{Color.BOLD}ESC{Color.RESET} at any time to stop immediately.
    """)
    pause()


def show_about():
    clear_screen()
    print_title("About")
    print(f"""
Essay Typewriter is a small typing-automation tool written by {Color.BOLD}Zexiang Zhang{Color.RESET}.
It reads text from content.txt and types it into whatever window currently
has focus, simulating a natural human typing rhythm — variable speed,
brief pauses at punctuation and spaces, and occasional realistic typos
that get corrected, similar to how a real person types.

The project is open source and contributions are welcome. Feel free to
open an issue, submit a pull request, or send a direct message if you
run into problems or have ideas for improvement.

{Color.CYAN}GitHub: https://github.com/626-Legendary/{Color.RESET}
    """)
    pause()


def show_settings():
    config = load_config()

    while True:
        speed_name = config.get("Typing", "speed", fallback="COLLEGE_STUDENT")
        speed_name = speed_name if speed_name in SPEED_ORDER else "COLLEGE_STUDENT"
        custom_wpm = config.getfloat("Typing", "custom_wpm", fallback=DEFAULT_CUSTOM_WPM)

        real_thinking = config.getboolean("Typing", "real_thinking", fallback=True)
        real_typing = config.getboolean("Typing", "real_typing", fallback=True)
        min_t = config.getfloat("Typing", "min_thinking_time", fallback=DEFAULT_MIN_THINKING)
        max_t = config.getfloat("Typing", "max_thinking_time", fallback=DEFAULT_MAX_THINKING)

        clear_screen()
        print_title("Settings")
        print(f"  {Color.YELLOW}{Color.BOLD}[1]{Color.RESET} Typing speed           : {Color.BOLD}{speed_label(speed_name, custom_wpm)}{Color.RESET}")
        thinking_suffix = f"  {Color.DIM}({min_t:g}s - {max_t:g}s){Color.RESET}" if real_thinking else ""
        print(f"  {Color.YELLOW}{Color.BOLD}[2]{Color.RESET} Real thinking          : {status_label(real_thinking)}{thinking_suffix}")
        print(f"  {Color.YELLOW}{Color.BOLD}[3]{Color.RESET} Typing errors          : {status_label(real_typing)}")
        print(f"  {Color.YELLOW}{Color.BOLD}[4]{Color.RESET} Back to main menu")
        print()

        choice = input("Select an option (1-4): ").strip()

        if choice == "1":
            print()
            print(f"{Color.BOLD}Typing speed:{Color.RESET}")
            for i, mode in enumerate(SPEED_ORDER, start=1):
                marker = f"{Color.GREEN}*{Color.RESET}" if mode == speed_name else " "
                print(f"  {marker} {i}. {speed_label(mode, custom_wpm)}")
            pick = input("Choose a speed (1-4): ").strip()

            if pick.isdigit() and 1 <= int(pick) <= len(SPEED_ORDER):
                selected = SPEED_ORDER[int(pick) - 1]
                if selected == "CUSTOM":
                    wpm_in = input(f"{Color.CYAN}Words per minute (WPM):{Color.RESET} ").strip()
                    try:
                        wpm_value = float(wpm_in)
                        if wpm_value <= 0:
                            raise ValueError
                        config.set("Typing", "custom_wpm", str(wpm_value))
                    except ValueError:
                        print(f"{Color.RED}[!] Invalid WPM, keeping previous custom speed.{Color.RESET}")
                        pause()
                config.set("Typing", "speed", selected)
                save_config(config)
            else:
                print(f"{Color.RED}[!] Invalid choice.{Color.RESET}")
                pause()

        elif choice == "2":
            new_state = not real_thinking
            config.set("Typing", "real_thinking", str(new_state).lower())
            if new_state:
                if not real_thinking:
                    # Turning it on from off: previous stored values were
                    # forced to 0/0, so offer the sensible defaults instead.
                    print(f"{Color.YELLOW}[i] Real thinking enabled. "
                          f"Default: min {DEFAULT_MIN_THINKING}s / max {DEFAULT_MAX_THINKING}s.{Color.RESET}")
                    suggested_min, suggested_max = DEFAULT_MIN_THINKING, DEFAULT_MAX_THINKING
                else:
                    suggested_min, suggested_max = min_t, max_t
                try:
                    min_in = input(f"Min thinking time in seconds [{suggested_min:g}]: ").strip()
                    max_in = input(f"Max thinking time in seconds [{suggested_max:g}]: ").strip()
                    new_min = float(min_in) if min_in else suggested_min
                    new_max = float(max_in) if max_in else suggested_max
                    if new_min < 0 or new_max < 0 or new_min > new_max:
                        raise ValueError
                    config.set("Typing", "min_thinking_time", str(new_min))
                    config.set("Typing", "max_thinking_time", str(new_max))
                except ValueError:
                    print(f"{Color.RED}[!] Invalid values, using defaults "
                          f"({DEFAULT_MIN_THINKING}s / {DEFAULT_MAX_THINKING}s).{Color.RESET}")
                    config.set("Typing", "min_thinking_time", str(DEFAULT_MIN_THINKING))
                    config.set("Typing", "max_thinking_time", str(DEFAULT_MAX_THINKING))
                    pause()
            else:
                config.set("Typing", "min_thinking_time", "0")
                config.set("Typing", "max_thinking_time", "0")
            save_config(config)

        elif choice == "3":
            config.set("Typing", "real_typing", str(not real_typing).lower())
            save_config(config)

        elif choice == "4":
            apply_config_to_runtime(config)
            return

        else:
            print(f"{Color.RED}[!] Invalid option.{Color.RESET}")
            pause()


# ---------------------------------------------------------------------------
# Typing logic
# ---------------------------------------------------------------------------

def stop_typing():
    global is_running
    print(f"\n{Color.RED}[!] ESC detected — stopping typing...{Color.RESET}")
    is_running = False


def start_typing():
    global is_running

    # print(f"DEBUG: TYPING_SPEED_MODE = {TYPING_SPEED_MODE}")
    # print(f"DEBUG: current_wpm() = {current_wpm()}")
    # print(f"DEBUG: SPEED_PRESET_WPM = {SPEED_PRESET_WPM}")

    if not files_exist():
        print(f"{Color.RED}[-] content.txt / config.ini not found in {BASE_DIR}.{Color.RESET}")
        print("    Please go to Settings, or restart the program to recreate them.")
        pause()
        return

    is_running = True

    clear_screen()
    print_title("Get Ready")
    print(f"{Color.YELLOW}Switch to your target window now — typing starts in:{Color.RESET}\n")
    for remaining in (5, 4, 3, 2, 1):
        if not is_running:
            return
        print(f"    {Color.BOLD}{remaining}...{Color.RESET}")
        time.sleep(1)
    print()

    with open(CONTENT_PATH, "r", encoding="utf-8") as file:
        while is_running:
            char = file.read(1)

            if not char:
                print(f"\n{Color.GREEN}[+] Typing finished!{Color.RESET}")
                pause()
                break

            print(char, end="", flush=True)

            if REAL_TYPING:
                simulate_mistake(char)

            base_interval = wpm_to_interval(current_wpm())
            print(" base_interval:", base_interval )

            if char in ".,?!":
                if REAL_THINKING:
                    simulate_thinking(min_thinking_time,max_thinking_time)
                actual_interval = base_interval + random.uniform(0.2, 0.4)
            elif char == " ":
                if REAL_THINKING:
                    simulate_thinking(min_thinking_time,max_thinking_time)
                actual_interval = base_interval + random.uniform(0.05, 0.15)
            else:
                actual_interval = max(0.02, random.gauss(base_interval, 0.03))

            if char == '\n':
                pyautogui.press('enter')
            else:
                pyautogui.write(char)
            time.sleep(actual_interval)


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    keyboard.add_hotkey('esc', stop_typing)

    if not ensure_setup():
        return 

    apply_config_to_runtime(load_config())

    while True:
        show_menu()
        choice = input("Select an option: ").strip().lower()

        if choice == '1':
            show_instructions()
        elif choice == '2':
            print(f"\n{Color.CYAN}[+] Preparing to start typing...{Color.RESET}")
            time.sleep(1)
            start_typing()
        elif choice == '3':
            show_settings()
        elif choice == '4':
            show_about()
        elif choice == 'q':
            print(f"\n{Color.CYAN}[+] Exiting program.{Color.RESET}")
            time.sleep(1)
            break
        else:
            print(f"\n{Color.RED}[!] Invalid option, please try again.{Color.RESET}")
            time.sleep(1)


if __name__ == "__main__":
    main()