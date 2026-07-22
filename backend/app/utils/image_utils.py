import cv2 as cv
import numpy as np

def decode_image(image_bytes: bytes)-> np.ndarray:
    nparr = np.frombuffer(image_bytes, np.uint8)
    img = cv.imdecode(nparr, cv.IMREAD_COLOR)

    if img is None:
        raise ValueError("Could not load image. File may be corrupted.")
    return img

def is_blurry(face_region:np.ndarray, threshold:float = 100.0)-> bool:
    gray = cv.cvtColor(face_region, cv.COLOR_BGR2GRAY)
    laplacian_var = cv.Laplacian(gray, cv.CV_64F).var()
    return laplacian_var < threshold

def crop_face(frame:np.ndarray, bbox:list, margin:float = 0.2)-> np.ndarray:
    x1,y1, x2, y2 = [int(v) for v in bbox]
    h, w = frame.shape[:2]

    margin_x = int((x2-x1) * margin)
    margin_y = int((y2-y1) * margin)

    x1 = max(0, x1 - margin_x)
    y1 = max(0, y1 - margin_y)
    x2 = min(w, x2 + margin_x)
    y2 = min(h, y2 + margin_y)

    return frame[y1:y2, x1:x2]