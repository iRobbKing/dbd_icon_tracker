from __future__ import annotations

import cv2
import numpy as np
import win32con
import win32gui
import win32ui


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


def take_screenshot_grey(*args, **kwargs):
    return make_grey(take_screenshot(*args, **kwargs))


def read_template(path):
    return make_grey(cv2.imread(path))


def match(picture, template, threshold):
    result = cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return list(zip(*locations[::-1]))
