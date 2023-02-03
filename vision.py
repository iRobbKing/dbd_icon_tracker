import cv2
import numpy as np
import win32con
import win32gui
import win32ui

class WinAPI:
    def __init__(self, window_name):
        self.window_name = window_name
        self.hwnd = self.__get_window_hwnd()
        self.w_dc = win32gui.GetWindowDC(self.hwnd)
        self.dc_obj = win32ui.CreateDCFromHandle(self.w_dc)
        self.c_dc = self.dc_obj.CreateCompatibleDC()
        self.data_bit_map = win32ui.CreateBitmap()

    def __get_window_hwnd(self):
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


class Vision:
    def __init__(self, window_name):
        self.window_name = window_name
        self.winapi = WinAPI(self.window_name)

    def get_screenshot(self, filename = None, grayscale = False):
        screenshot = None
        if filename == None:
            screenshot = self.winapi.get_screenshot()
        else:
            screenshot = cv2.imread(filename)
        if grayscale:
            screenshot = cv2.cvtColor(screenshot, cv2.COLOR_RGB2GRAY)
        return screenshot
    
def read_picture_from_file(path):
    return cv2.imread(path)

def take_screenshot(x, y, w, h, hwnd=0):
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


def match(picture, template, threshold):
    result = cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED)
    locations = np.where(result >= threshold)
    return list(zip(*locations[::-1]))
