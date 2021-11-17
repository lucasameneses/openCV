import numpy as np
import cv2
import time
from tqdm import tqdm


def onChange(value):
    pass


img = cv2.imread("test.jpg",cv2.IMREAD_GRAYSCALE)
copy_img = img.copy()

# Edge
edge_img = cv2.Canny(copy_img, 100,400)
cv2.imwrite('edge.jpg',edge_img)

windowTitle = "Ajuste de Brilho e Contraste"
cv2.namedWindow(windowTitle)

cv2.createTrackbar("contraste", windowTitle, 100, 100, onChange)
cv2.createTrackbar("brilho", windowTitle, 0, 100, onChange)

before_contrast = 100
update_contrast = False

before_brightness = 0
update_brightness = False

before_min_hue = 0
update_min_hue = False

before_max_hue = 0
update_max_hue = False

counter_time = 0

while True:
    current_contrast = cv2.getTrackbarPos("contraste", windowTitle)
    current_brightness = cv2.getTrackbarPos("brilho", windowTitle)

    if before_contrast != current_contrast:
        update_contrast = True
        counter_time = time.time()
        before_contrast = current_contrast

    if before_brightness != current_brightness:
        update_brightness = True
        counter_time = time.time()
        before_brightness = current_brightness

    if time.time() - counter_time > 1:
        if update_contrast or update_brightness:
            copy_img = cv2.convertScaleAbs(img, alpha=current_contrast / 100, beta=current_brightness)

            update_contrast = False
            update_brightness = False

    # Retangulo
    dot1 = (60, 70)
    dot2 = (90, 190)
    copy_img = cv2.rectangle(copy_img, dot1, dot2, (0, 0, 0), 2)

    # Texto
    text = "Test "
    dot = (300, 200)
    copy_img = cv2.putText(copy_img, text, dot, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), cv2.LINE_4)

    # Zoom
    # cropped = copy_img[40:400, 60:600]

    # Edge
    # copy_img = cv2.Canny(copy_img, 0, 200)

    # LUT
    lut_img = cv2.applyColorMap(copy_img,cv2.COLORMAP_RAINBOW)
    cv2.imwrite('lut.jpg',lut_img)
    

    cv2.imshow(windowTitle, edge_img)

    keyPressed = cv2.waitKey(1) & 0xFF
    if keyPressed == 27:
        break

cv2.destroyAllWindows()
