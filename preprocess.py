import cv2
import numpy as np

def preprocess_image(path):

    img=cv2.imread(path)

    if img is None:
        raise FileNotFoundError(path)

    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    gray=cv2.fastNlMeansDenoising(gray)

    clahe=cv2.createCLAHE(2.0,(8,8))
    gray=clahe.apply(gray)

    blur=cv2.GaussianBlur(gray,(3,3),0)

    processed=cv2.cvtColor(blur,cv2.COLOR_GRAY2BGR)

    return processed