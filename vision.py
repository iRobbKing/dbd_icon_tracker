import cv2
import numpy as np
import win32con
import win32gui
import win32ui


def _get_window_hwnd(title):
    dbd_hwnd = 0

    def inner(hwnd, _):
        nonlocal dbd_hwnd

        text = win32gui.GetWindowText(hwnd)
        if title in text:
            dbd_hwnd = hwnd

    win32gui.EnumWindows(inner, '')
    return dbd_hwnd


def read_picture_from_file(path):
    return cv2.imread(path)


def take_screenshot(x, y, w, h, hwnd=None):
    w_dc = win32gui.GetWindowDC(hwnd)
    dc_obj = win32ui.CreateDCFromHandle(w_dc)
    c_dc = dc_obj.CreateCompatibleDC()
    data_bit_map = win32ui.CreateBitmap()
    data_bit_map.CreateCompatibleBitmap(dc_obj, w, h)
    c_dc.SelectObject(data_bit_map)
    c_dc.BitBlt((0, 0), (w, h), dc_obj, (x, y), win32con.SRCCOPY)

    signed_ints_array = data_bit_map.GetBitmapBits(True)
    img = np.fromstring(signed_ints_array, dtype='uint8')
    img.shape = (h, w, 4)

    dc_obj.DeleteDC()
    c_dc.DeleteDC()
    win32gui.ReleaseDC(hwnd, w_dc)
    win32gui.DeleteObject(data_bit_map.GetHandle())

    return np.ascontiguousarray(img[..., :3])


def make_grey(picture):
    return cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)


def match(picture, template):
    return cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED)
