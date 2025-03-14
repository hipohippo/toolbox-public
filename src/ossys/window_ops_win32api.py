import ctypes

user32 = ctypes.windll.user32
from ctypes import wintypes

# Define the necessary constants and types
GWL_STYLE = -16
GW_CHILD = 5
GW_HWNDNEXT = 2
ES_MULTILINE = 0x4
ES_PASSWORD = 0x20
ES_READONLY = 0x800
WS_VISIBLE = 0x10000000
WM_GETTEXT = 0x000D
WM_GETTEXTLENGTH = 0x000E

HWND = ctypes.wintypes.HWND
LPARAM = ctypes.wintypes.LPARAM

WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)

# Retrieve the handle of the target window
window_title = "chrome"
hwnd = ctypes.windll.user32.FindWindowW(None, window_title)

# Retrieve the handle of the textbox within the window
textbox_hwnd = ctypes.windll.user32.GetWindow(hwnd, GW_CHILD)
while textbox_hwnd:
    style = ctypes.windll.user32.GetWindowLongW(textbox_hwnd, GWL_STYLE)
    if style & ES_MULTILINE or style & ES_PASSWORD or style & ES_READONLY:
        textbox_hwnd = ctypes.windll.user32.GetWindow(textbox_hwnd, GW_HWNDNEXT)
        continue
    if style & WS_VISIBLE:
        break
    textbox_hwnd = ctypes.windll.user32.GetWindow(textbox_hwnd, GW_HWNDNEXT)

# Retrieve the text from the textbox
text_length = (
    ctypes.windll.user32.SendMessageW(textbox_hwnd, WM_GETTEXTLENGTH, 0, 0) + 1
)
buffer = ctypes.create_unicode_buffer(text_length)
ctypes.windll.user32.SendMessageW(textbox_hwnd, WM_GETTEXT, text_length, LPARAM(buffer))
text = buffer.value


def enum_windows_callback(hwnd, lParam):
    # window_title = ctypes.create_unicode_buffer(1024)
    # ctypes.windll.user32.GetWindowTextW(hwnd, window_title, ctypes.sizeof(window_title))
    pid = ctypes.windll.user32.GetWindowThreadProcessId(hwnd, 0)
    print(pid)
    return True


WNDENUMPROC = ctypes.WINFUNCTYPE(wintypes.BOOL, wintypes.HWND, wintypes.LPARAM)
user32 = ctypes.windll.user32
user32.EnumWindows.argtypes = [WNDENUMPROC, wintypes.LPARAM]
user32.GetWindowTextLengthW.argtypes = [wintypes.HWND]
user32.GetWindowTextW.argtypes = [wintypes.HWND, wintypes.LPWSTR, ctypes.c_int]


def worker(hwnd, lParam):
    length = user32.GetWindowTextLengthW(hwnd) + 1
    buffer = ctypes.create_unicode_buffer(length)
    user32.GetWindowTextW(hwnd, buffer, length)
    if repr(buffer.value).lower().find("deepl") >= 0:
        print(hwnd, repr(buffer.value))
    return True


cb_worker = WNDENUMPROC(worker)
if not user32.EnumWindows(cb_worker, 42):
    raise ctypes.WinError()
