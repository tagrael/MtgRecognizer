import numpy as np
import cv2

BKG_THRESH = 60
CARD_MAX_AREA = 1200000
CARD_MIN_AREA = 25000


def preprocess_image(image, white_background=1):
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    if white_background == 0:
        blur = cv2.GaussianBlur(gray, (5, 5), 0)

        img_w, img_h = np.shape(image)[:2]
        bkg_level = gray[int(img_h / 100)][int(img_w / 2)]
        thresh_level = bkg_level + BKG_THRESH

        retval, thresh = cv2.threshold(blur, thresh_level, 255, cv2.THRESH_BINARY)

        return thresh

    else:
        retval, thresh = cv2.threshold(gray, 70, 255, cv2.THRESH_BINARY)
        return thresh


def find_cards(thresh_image):

    cnts, hier = cv2.findContours(thresh_image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    index_sort = sorted(range(len(cnts)), key=lambda i: cv2.contourArea(cnts[i]), reverse=True)

    if len(cnts) == 0:
        return []

    cnts_sort = []
    hier_sort = []
    cnt_is_card = np.zeros(len(cnts), dtype=int)

    for i in index_sort:
        cnts_sort.append(cnts[i])
        hier_sort.append(hier[0][i])

    result = []

    for i in range(len(cnts_sort)):
        size = cv2.contourArea(cnts_sort[i])
        peri = cv2.arcLength(cnts_sort[i], True)
        approx = cv2.approxPolyDP(cnts_sort[i], 0.05 * peri, True)

        if CARD_MAX_AREA > size > CARD_MIN_AREA and (hier_sort[i][3] == -1 or hier_sort[i][3] == 0):
            cnt_is_card[i] = 1
            result.append(cnts_sort[i])

    # print(str(max(map(cv2.contourArea, result))))
    return result


def crop_contour(image, contour):
    # gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # mask = np.zeros_like(gray)
    # cv2.drawContours(mask, contour, -1, 255, -1)
    # out = np.zeros_like(gray)
    # out[mask == 255] = gray[mask == 255]
    #
    # (y, x) = np.where(mask == 255)
    # (topy, topx) = (np.min(y), np.min(x))
    # (bottomy, bottomx) = (np.max(y), np.max(x))
    # return out[topy:bottomy+1, topx:bottomx+1]

    rect = cv2.minAreaRect(contour)
    center, size, theta = rect
    center, size = tuple(map(int, center)), tuple(map(int, size))
    # Get rotation matrix for rectangle
    matrix = cv2.getRotationMatrix2D(center, theta, 1)
    # Perform rotation on src image
    dst = cv2.warpAffine(image, matrix, image.shape[:2])
    out = cv2.getRectSubPix(dst, size, center)
    return out
