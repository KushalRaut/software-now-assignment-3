import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2

from image_manager import ImageManager

class ImageProcessor:
    def __init__(self):
        self.image = None
        self.original_image = None

    def load_image(self, file_path):
        self.image = cv2.imread(file_path)
        if self.image is None:
            raise ValueError("Could not load image")
        self.original_image = self.image.copy()
        return self.image

    def save_image(self, file_path):
        if self.image is not None:
            cv2.imwrite(file_path, self.image)
        else:
            raise ValueError("No image to save")

    def grayscale(self):
        if self.image is not None:
            self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)
            return self.image

    def blur(self, intensity=5):
        if self.image is not None:
            self.image = cv2.GaussianBlur(self.image, (intensity, intensity), 0)
            return self.image

    def edge_detection(self):
        if self.image is not None:
            self.image = cv2.Canny(self.image, 100, 200)
            return self.image

    def adjust_brightness(self, value):
        if self.image is not None:
            hsv = cv2.cvtColor(self.image, cv2.COLOR_BGR2HSV)
            h, s, v = cv2.split(hsv)
            v = cv2.add(v, value)
            final_hsv = cv2.merge((h, s, v))
            self.image = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
            return self.image

    def adjust_contrast(self, value):
        if self.image is not None:
            alpha = value / 100.0
            self.image = cv2.convertScaleAbs(self.image, alpha=alpha, beta=0)
            return self.image

    def rotate(self, angle):
        if self.image is not None:
            (h, w) = self.image.shape[:2]
            center = (w // 2, h // 2)
            M = cv2.getRotationMatrix2D(center, angle, 1.0)
            self.image = cv2.warpAffine(self.image, M, (w, h))
            return self.image

    def flip(self, direction):
        if self.image is not None:
            if direction == 'horizontal':
                self.image = cv2.flip(self.image, 1)
            elif direction == 'vertical':
                self.image = cv2.flip(self.image, 0)
            return self.image

    def resize(self, scale):
        if self.image is not None:
            (h, w) = self.image.shape[:2]
            scale_pct = float(scale) / 100.0
            new_h = max(1, int(h * scale_pct))
            new_w = max(1, int(w * scale_pct))
            self.image = cv2.resize(self.image, (new_w, new_h), interpolation=cv2.INTER_AREA)
            return self.image

    def get_image(self):
        return self.image

    def reset(self):
        if self.original_image is not None:
            self.image = self.original_image.copy()

class UndoRedoManager:
    def __init__(self):
        self.history = []
        self.redo_stack = []

    def save_state(self, image):
        self.history.append(image.copy())
        self.redo_stack.clear()  # Clear redo stack on new action

    def undo(self, current=None):
        if self.history:
            if current is not None:
                self.redo_stack.append(current.copy())
            return self.history.pop()
        return None

    def redo(self):
        if self.redo_stack:
            next_state = self.redo_stack.pop()
            self.history.append(next_state)
            return next_state
        return None

class Toolbar(tk.Frame):
    def __init__(self, master, app):
        super().__init__(master)
        self.app = app
        self.create_widgets()

    def create_widgets(self):
        # Buttons for effects
        tk.Button(self, text="Grayscale", command=self.app.apply_grayscale).pack(fill=tk.X)
        tk.Button(self, text="Blur", command=self.app.apply_blur).pack(fill=tk.X)
        tk.Button(self, text="Edge Detection", command=self.app.apply_edge_detection).pack(fill=tk.X)

        # Sliders
        self.brightness_slider = tk.Scale(self, from_=-255, to=255, orient=tk.HORIZONTAL, label="Brightness")
        self.brightness_slider.bind("<ButtonRelease-1>", lambda e: self.app.apply_brightness(self.brightness_slider.get()))
        self.brightness_slider.pack(fill=tk.X)

        self.contrast_slider = tk.Scale(self, from_=0, to=200, orient=tk.HORIZONTAL, label="Contrast")
        self.contrast_slider.bind("<ButtonRelease-1>", lambda e: self.app.apply_contrast(self.contrast_slider.get()))
        self.contrast_slider.pack(fill=tk.X)

        self.scale_slider = tk.Scale(self, from_=10, to=200, orient=tk.HORIZONTAL, label="Scale (%)")
        self.scale_slider.set(100)
        self.scale_slider.bind("<ButtonRelease-1>", lambda e: self.app.apply_resize(self.scale_slider.get()))
        self.scale_slider.pack(fill=tk.X)

        # Rotation buttons
        tk.Button(self, text="Rotate 90°", command=lambda: self.app.apply_rotate(90)).pack(fill=tk.X)
        tk.Button(self, text="Rotate 180°", command=lambda: self.app.apply_rotate(180)).pack(fill=tk.X)
        tk.Button(self, text="Rotate 270°", command=lambda: self.app.apply_rotate(270)).pack(fill=tk.X)

        # Flip buttons
        tk.Button(self, text="Flip Horizontal", command=lambda: self.app.apply_flip('horizontal')).pack(fill=tk.X)
        tk.Button(self, text="Flip Vertical", command=lambda: self.app.apply_flip('vertical')).pack(fill=tk.X)

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Image Editor")
        self.geometry("800x600")

        self.processor = ImageProcessor()
        self.undo_manager = UndoRedoManager()
        self.manager = ImageManager()
        self.current_file = None

        self.create_menu()
        self.create_widgets()
        self.status_bar = tk.Label(self, text="No image loaded", relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def create_menu(self):
        menubar = tk.Menu(self)
        filemenu = tk.Menu(menubar, tearoff=0)
        filemenu.add_command(label="Open", command=self.open_image)
        filemenu.add_command(label="Save", command=self.save_image)
        filemenu.add_command(label="Save As", command=self.save_as_image)
        filemenu.add_separator()
        filemenu.add_command(label="Exit", command=self._confirm_exit)
        menubar.add_cascade(label="File", menu=filemenu)

        editmenu = tk.Menu(menubar, tearoff=0)
        editmenu.add_command(label="Undo", command=self.undo)
        editmenu.add_command(label="Redo", command=self.redo)
        menubar.add_cascade(label="Edit", menu=editmenu)

        self.config(menu=menubar)

    def _confirm_exit(self):
        if messagebox.askokcancel("Exit", "Do you want to exit?"):
            self.quit()

    def create_widgets(self):
        self.toolbar = Toolbar(self, self)
        self.toolbar.pack(side=tk.LEFT, fill=tk.Y)

        self.image_label = tk.Label(self)
        self.image_label.pack(expand=True, fill=tk.BOTH)

    def open_image(self):
        file_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.png *.bmp")])
        if file_path:
            try:
                image = self.processor.load_image(file_path)
                self.manager.load_image(file_path)
                self.undo_manager.save_state(image)
                self.current_file = file_path
                self.display_image()
                self.update_status()
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def save_image(self):
        if self.current_file:
            try:
                self.processor.save_image(self.current_file)
                messagebox.showinfo("Success", "Image saved successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))
        else:
            self.save_as_image()

    def save_as_image(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".jpg", filetypes=[("JPEG", "*.jpg"), ("PNG", "*.png"), ("BMP", "*.bmp")])
        if file_path:
            try:
                self.processor.save_image(file_path)
                self.current_file = file_path
                self.manager._filepath = file_path
                messagebox.showinfo("Success", "Image saved successfully")
            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def display_image(self):
        image = self.processor.get_image()
        if image is not None:
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            self.photo = ImageTk.PhotoImage(pil_image)
            self.image_label.config(image=self.photo)

    def update_status(self):
        self.status_bar.config(text=self.manager.get_info())

    def apply_effect(self, func, *args):
        current_image = self.processor.get_image()
        if current_image is None:
            messagebox.showerror("Error", "Please open an image first.")
            return
        self.undo_manager.save_state(current_image)
        func(*args)
        self.manager._image = self.processor.get_image()
        self.display_image()
        self.update_status()

    def apply_grayscale(self):
        self.apply_effect(self.processor.grayscale)

    def apply_blur(self):
        intensity = 5  # Default or could prompt
        self.apply_effect(self.processor.blur, intensity)

    def apply_edge_detection(self):
        self.apply_effect(self.processor.edge_detection)

    def apply_brightness(self, value):
        self.apply_effect(self.processor.adjust_brightness, value)

    def apply_contrast(self, value):
        self.apply_effect(self.processor.adjust_contrast, value)

    def apply_rotate(self, angle):
        self.apply_effect(self.processor.rotate, angle)

    def apply_flip(self, direction):
        self.apply_effect(self.processor.flip, direction)

    def apply_resize(self, scale=None):
        val = float(self.toolbar.scale_slider.get()) if scale is None else float(scale)
        self.apply_effect(self.processor.resize, val)

    def undo(self):
        state = self.undo_manager.undo(self.processor.get_image())
        if state is not None:
            self.processor.image = state
            self.manager._image = state
            self.display_image()
            self.update_status()

    def redo(self):
        state = self.undo_manager.redo()
        if state is not None:
            self.processor.image = state
            self.manager._image = state
            self.display_image()
            self.update_status()

if __name__ == "__main__":
    app = App()   
    app.mainloop()            