import cv2


def show_image_in_window(window_name, image):
    try:
        cv2.getWindowProperty(window_name, cv2.WND_PROP_AUTOSIZE)
    except cv2.error:
        cv2.namedWindow(window_name, cv2.WINDOW_NORMAL)
        cv2.resizeWindow(window_name, 450, 300)
        cv2.setWindowProperty(window_name, cv2.WND_PROP_TOPMOST, 1)
    else:
        cv2.imshow(window_name, image)


def wait(delay):
    cv2.waitKey(delay)


def read_image(path):
    return cv2.imread(path)


def make_gray(picture):
    return cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)


def match(picture, template, mask):
    return cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED, mask=mask)
