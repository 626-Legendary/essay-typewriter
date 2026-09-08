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

COMMON_PREPS= {
    "at","in","for","of","on","from","by","between","after","before","near","under","since","during","below","with","though"
    }

TRANSITIONS ={
    "and","also","too","as well as","in addition","additionally","futhermore","moreover","besides","not only","but also","however","nevertheless","nonetheless","even though","whereas","while","on the other hand","in contrast","conversely","yet","due to","owing to","fisrt of all","to begin with","initially","for instance","for example","such as","like","e.g.","particularly"
    }

def get_random_neighbor_char(char):
    """Get a QWERTY-neighboring key; fall back to a random letter."""
    char = char.lower()
    if char in QWERTY_MAP:
        return random.choice(QWERTY_MAP[char])
    return chr(random.randint(97, 122))

def get_random_prep():
    prep = random.choice(list(COMMON_PREPS))
    return prep, len(prep)

def get_random_transition():
    tran = random.choice(list(TRANSITIONS))
    return tran,len(tran)

def simulate_thinking(min,max):
    thinking_time = random.uniform(min, max)
    time.sleep(thinking_time)

'''
替换错误(把要打的键换成了另一个，通常是相邻键) 33%
插入错误(在正确字符旁边多按了一个相邻键) 39% 
删除错误(漏打了某个字符) 18%
颠倒错误(交换了两个相邻字符，尤其常见于需要左右手配合切换的场景) 11%
'''

def simulate_mistake(char):
    r = random.random()  # 0.0 - 1.0

    if r <= 0.08:
        input_error1(char)
    elif r<= 0.09:
        input_error2(char)
    elif r<= 0.11:
        input_error3(char)
    elif r<= 0.21:
        input_error4(char)
    elif r<= 0.23:
        input_error5(char)
    elif r<= 0.24:
        input_error6(char)
    elif r<= 0.25:
        input_error7(char)
    elif r<= 0.33:
        input_error8(char)
    

 
def input_error1(char): # 替换错误 33% => 8%
    pyautogui.press(get_random_neighbor_char(char))
    time.sleep(0.3)
    pyautogui.press('backspace')

def input_error2(char): # 回车 + 退格 # 1%
    pyautogui.press('enter')
    time.sleep(0.6)
    pyautogui.press('backspace')

def input_error3(char): # 随机 介词 # 2%
    if char == " ":
        prep, length = get_random_prep()
        pyautogui.write(prep,interval=0.2)
        time.sleep(0.5)
        pyautogui.press('backspace',presses=length,interval=0.1)

def input_error4(char): # 插入错误 39% => 10%
    pyautogui.press(char)
    time.sleep(0.1)
    pyautogui.press(get_random_neighbor_char(char))
    time.sleep(0.3)
    pyautogui.press('backspace',presses=2,interval=0.1)

def input_error5(char): # 随机 连接词 # 2%
    if char in ",.?;":
        tran, length = get_random_transition()
        pyautogui.write(tran,interval=0.25)
        time.sleep(0.5)
        pyautogui.press('backspace',presses=length,interval=0.15)

def input_error6(char): # 1%
    if char == ".":
        pyautogui.press('capslock')
        time.sleep(0.1)
        pyautogui.press('space')
        time.sleep(0.2)
        pyautogui.press(chr(random.randint(65, 90)))
        time.sleep(0.1)
        pyautogui.press('capslock')
        time.sleep(0.3)
        pyautogui.press('backspace')
        time.sleep(0.1)
        pyautogui.press('backspace')

def input_error7(char): # 1%
    if char == ".":
        time.sleep(1)
        pyautogui.press('space')
        pyautogui.press('space')
        time.sleep(3)
        pyautogui.press('backspace')
        time.sleep(0.1)
        pyautogui.press('backspace')

def input_error8(char): # 5%
    if char == "<":
        pyautogui.press(',')
        time.sleep(0.2)
        pyautogui.press('backspace')
    elif char == ">":
        pyautogui.press('.')
        time.sleep(0.2)
        pyautogui.press('backspace')
    elif char == "?":
        pyautogui.press('/')
        time.sleep(0.2)
        pyautogui.press('backspace')
    elif char == "{":
        pyautogui.press('[')
        time.sleep(0.2)
        pyautogui.press('backspace')
    elif char == "}":
        pyautogui.press(']')
        time.sleep(0.2)
        pyautogui.press('backspace')
    
def input_error9(char):
    pass
def input_error10(char):
    pass
