import numpy as np
import win32con
import win32gui
import win32ui

class WinAPI:
    def __init__(self, window_name):
        self.window_name = window_name
        self.hwnd = self._get_window_hwnd()
        self.window_device_context = win32gui.GetWindowDC(self.hwnd)
        self.device_context = win32ui.CreateDCFromHandle(self.window_device_context)
        self.compatible_device_context = self.device_context.CreateCompatibleDC()
        self.bitmap = win32ui.CreateBitmap()

    def _get_window_hwnd(self):
        dbd_hwnd = 0
        def inner(hwnd, _):
            nonlocal dbd_hwnd
            text = win32gui.GetWindowText(hwnd)
            if self.window_name in text:
                dbd_hwnd = hwnd
        win32gui.EnumWindows(inner, '')
        return dbd_hwnd

    def get_screenshot(self, x, y, w, h):  
        self.bitmap.CreateCompatibleBitmap(self.device_context, w, h)
        self.compatible_device_context.SelectObject(self.bitmap)
        self.compatible_device_context.BitBlt((0, 0), (w, h), self.device_context, (x, y), win32con.SRCCOPY)
        signed_ints_array = self.bitmap.GetBitmapBits(True)
        win32gui.DeleteObject(self.bitmap.GetHandle())
        img = np.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (h, w, 4)
        return img[:,:,:3]

    def __del__(self):
        self.device_context.DeleteDC()
        self.compatible_device_context.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.window_device_context)
