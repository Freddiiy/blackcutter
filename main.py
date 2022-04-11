import errno

import cv2 as cv
from os import listdir, getcwd, mkdir, path


def crop_img(img_to_be_cropped: str):
    img = cv.imread(img_to_be_cropped)
    grayscale = cv.cvtColor(img, cv.COLOR_RGB2GRAY)
    _, thresh = cv.threshold(grayscale, 1, 255, cv.THRESH_BINARY)

    contours, hierarchy = cv.findContours(thresh, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    cnt = contours[0]
    x, y, w, h = cv.boundingRect(cnt)

    crop = img[y:y + h, x:x + w]

    splitend = img_to_be_cropped.split(".")

    path_to_make = f"{getcwd()}/cropped"

    try:
        if not path.exists(path_to_make):
            mkdir(path_to_make)
    except OSError as e:
        if e.errno != errno.EEXIST:
            raise

    cv.imwrite(f"{path_to_make}/{splitend[0]}_cropped.png", crop)
    print(f"cropped: {img_to_be_cropped}")


def crop_imgs(imgs: list):
    for img in imgs:
        crop_img(img)


def get_files():
    dir_list = []
    for file in listdir():
        if file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".bmp"):
            dir_list.append(file)

    return dir_list


if __name__ == '__main__':
    crop_imgs(get_files())
