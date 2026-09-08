import time
import pyautogui
import random

# ---------------------------------------------------------------------------
# Neighboring Keys Mapping ( typo-simulation logic )
# ---------------------------------------------------------------------------

QWERTY_MAP = {
    'a': 'qwsz', 'b': 'vghn', 'c': 'xdfv', 'd': 'erfcxs',
    'e': 'wsdr34', 'f': 'rtgvcd', 'g': 'tyhbvf', 'h': 'yujngb',
    'i': 'ujko98', 'j': 'uiknhm', 'k': 'iojlm,', 'l': 'opk,;.',
    'm': 'njk,', 'n': 'bhjm', 'o': 'iklp09', 'p': 'ol[0-',
    'q': 'wa12', 'r': 'e45dft', 's': 'awedxz', 't': 'r56yfg',
    'u': 'y78jhi', 'v': 'cfgb', 'w': 'qase32', 'x': 'zsdc',
    'y': 't67uhg', 'z': 'asx'
}

def get_random_neighbor_char(char):
    """Get a QWERTY-neighboring key; fall back to a random letter."""
    char = char.lower()
    if char in QWERTY_MAP:
        return random.choice(QWERTY_MAP[char])
    return chr(random.randint(97, 122))

def simulate_thinking(min,max):
    thinking_time = random.uniform(min, max)
    time.sleep(thinking_time)


def simulate_mistake(char):
    r = random.random()  # 0.0 - 1.0

    if r <= 0.2:
        pyautogui.write(get_random_neighbor_char(char), interval=0.4)
        pyautogui.press('backspace')
    elif r <= 0.25:
        pyautogui.write(get_random_neighbor_char(char), interval=0.3)
        pyautogui.write(get_random_neighbor_char(char), interval=0.2)
        pyautogui.write(get_random_neighbor_char(char), interval=0.4)
        pyautogui.write(get_random_neighbor_char(char), interval=0.6)
        pyautogui.press('backspace')
        pyautogui.press('backspace')
        pyautogui.press('backspace')
        pyautogui.press('backspace')
    elif r <= 0.30:
        pyautogui.write(get_random_neighbor_char(char), interval=0.4)
        pyautogui.write(get_random_neighbor_char(char), interval=0.3)
        time.sleep(0.2)
        pyautogui.press('backspace')
        pyautogui.press('backspace')
        time.sleep(0.2)
        pyautogui.write(get_random_neighbor_char(char), interval=0.2)
        pyautogui.press('backspace')