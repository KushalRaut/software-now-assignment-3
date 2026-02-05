import cv2


class ImageProcessor:
    def __init__(self):
        pass

    def to_grayscale(self, image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    def blur(self, image, intensity):
        if intensity % 2 == 0:
            intensity += 1
        return cv2.GaussianBlur(image, (intensity, intensity), 0)

    def edge_detection(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return cv2.Canny(gray, 100, 200)

    def adjust_brightness(self, image, value):
        return cv2.convertScaleAbs(image, alpha=1, beta=value)

    def adjust_contrast(self, image, value):
        return cv2.convertScaleAbs(image, alpha=value, beta=0)

    def rotate(self, image, angle):
        if angle == 90:
            return cv2.rotate(image, cv2.ROTATE_90_CLOCKWISE)
        if angle == 180:
            return cv2.rotate(image, cv2.ROTATE_180)
        if angle == 270:
            return cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
        return image

    def flip(self, image, direction):
        if direction == "horizontal":
            return cv2.flip(image, 1)
        if direction == "vertical":
            return cv2.flip(image, 0)
        return image

    def resize(self, image, width, height):
        return cv2.resize(image, (width, height))
