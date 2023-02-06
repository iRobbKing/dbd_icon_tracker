import cv2

def create_window(winname):
    cv2.namedWindow(winname, cv2.WINDOW_NORMAL)
    cv2.resizeWindow(winname, 450, 300)
    cv2.setWindowProperty(winname, cv2.WND_PROP_TOPMOST, 1)

def set_title(winname, title):
    cv2.setWindowTitle(winname, title)

def show(winname, image):
    cv2.imshow(winname, image)
    cv2.waitKey(1)
    
def read_template(path):
    return cv2.cvtColor(cv2.imread(path), cv2.COLOR_RGB2GRAY)

def read_mask(path):
    return cv2.imread(path, cv2.IMREAD_GRAYSCALE)

def make_gray(picture):
    return cv2.cvtColor(picture, cv2.COLOR_RGB2GRAY)

def match(picture, template, mask):
    return cv2.matchTemplate(picture, template, cv2.TM_CCOEFF_NORMED, mask=mask)