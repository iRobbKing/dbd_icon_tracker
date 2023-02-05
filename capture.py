import numpy as np
import win32con
import win32gui
import win32ui

class WinAPI:
    def __init__(self, window_name):
        self.window_name = window_name
        self.hwnd = self._get_window_hwnd()
        self.w_dc = win32gui.GetWindowDC(self.hwnd)
        self.dc_obj = win32ui.CreateDCFromHandle(self.w_dc)
        self.c_dc = self.dc_obj.CreateCompatibleDC()
        self.data_bit_map = win32ui.CreateBitmap()

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
        self.data_bit_map.CreateCompatibleBitmap(self.dc_obj, w, h)
        self.c_dc.SelectObject(self.data_bit_map)
        self.c_dc.BitBlt((0, 0), (w, h), self.dc_obj, (x, y), win32con.SRCCOPY)

        signed_ints_array = self.data_bit_map.GetBitmapBits(True)
        img = np.fromstring(signed_ints_array, dtype='uint8')
        img.shape = (h, w, 4)
        return img[:,:,:3]

    def __del__(self):
        self.dc_obj.DeleteDC()
        self.c_dc.DeleteDC()
        win32gui.ReleaseDC(self.hwnd, self.w_dc)
        win32gui.DeleteObject(self.data_bit_map.GetHandle())
