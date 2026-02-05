import cv2
import os
import copy


class ImageManager:
    def __init__(self):
        self._image = None
        self._filepath = None
        self._history = []
        self._redo = []

    def load_image(self, filepath):
        self._filepath = filepath
        self._image = cv2.imread(filepath)
        self._history.clear()
        self._redo.clear()
        return self._image

    def commit(self, image):
        if self._image is not None:
            self._history.append(copy.deepcopy(self._image))
            self._redo.clear()
        self._image = image

    def undo(self):
        if self._history:
            self._redo.append(self._image)
            self._image = self._history.pop()
        return self._image

    def redo(self):
        if self._redo:
            self._history.append(self._image)
            self._image = self._redo.pop()
        return self._image

    def get_image(self):
        return self._image

    def save_image(self, filepath=None):
        if filepath:
            self._filepath = filepath
        if self._image is not None:
            cv2.imwrite(self._filepath, self._image)

    def get_info(self):
        if self._image is None:
            return "No image loaded"
        h, w = self._image.shape[:2]
        name = os.path.basename(self._filepath) if self._filepath else "Untitled"
        return f"{name}   {w} x {h}"
