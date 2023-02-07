import numpy as np
import win32con
import win32gui
import win32ui


def _get_window_hwnd(window_name):
    dbd_hwnd = 0

    def inner(hwnd, _):
        nonlocal dbd_hwnd
        text = win32gui.GetWindowText(hwnd)
        if window_name in text:
            dbd_hwnd = hwnd

    win32gui.EnumWindows(inner, '')
    return dbd_hwnd


class WinAPI:
    def __init__(self, window_name):
        self.hwnd = _get_window_hwnd(window_name)

    def __enter__(self):
        self.window_device_context = win32gui.GetWindowDC(self.hwnd)
        self.device_context = win32ui.CreateDCFromHandle(self.window_device_context)
        self.compatible_device_context = self.device_context.CreateCompatibleDC()
        self.bitmap = win32ui.CreateBitmap()

        def get_screenshot(x, y, w, h):
            self.bitmap.CreateCompatibleBitmap(self.device_context, w, h)
            self.compatible_device_context.SelectObject(self.bitmap)
            self.compatible_device_context.BitBlt((0, 0), (w, h), self.device_context, (x, y), win32con.SRCCOPY)
            signed_ints_array = self.bitmap.GetBitmapBits(True)
            win32gui.DeleteObject(self.bitmap.GetHandle())
            img = np.fromstring(signed_ints_array, dtype='uint8')
            img.shape = (h, w, 4)
            return img[:, :, :3]

        return get_screenshot

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.device_context.DeleteDC()
        self.compatible_device_context.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.window_device_context)
