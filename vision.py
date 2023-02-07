import cv2


def create_window(window_name):
    cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(window_name, 450, 300)
    cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)


def set_window_name(window_name, new_name):
    cv2.setWindowTitle(window_name, new_name)


def show_image_in_window(window_name, image, delay):
    cv2.imshow(window_name, image)
    cv2.waitKey(delay)


def read_image(path):
    return cv2.imread(path)


def make_gray(picture):
    return cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)


def match(picture, template, mask):
    return cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED, mask=mask)
