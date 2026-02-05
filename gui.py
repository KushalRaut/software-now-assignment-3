import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import cv2
import os

from image_manager import ImageManager
from image_processor import ImageProcessor


class ImageEditorGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("OpenCV Image Editor")
        self.root.geometry("1200x750")

        self.manager = ImageManager()
        self.processor = ImageProcessor()

        self.original_image = None
        self.preview_image = None

        self.load_icons()
        self.create_menu()
        self.create_layout()
        self.bind_shortcuts()

    # ================= ICONS =================

    def load_icons(self):
        self.icons = {}
        icon_dir = "assets/icons"

        def load(name):
            path = os.path.join(icon_dir, name)
            return ImageTk.PhotoImage(Image.open(path)) if os.path.exists(path) else None

        self.icons["open"] = load("open.png")
        self.icons["save"] = load("save.png")
        self.icons["save_as"] = load("save_as.png")
        self.icons["exit"] = load("exit.png")
        self.icons["undo"] = load("undo.png")
        self.icons["redo"] = load("redo.png")

    # ================= MENU =================

    def create_menu(self):
        menubar = tk.Menu(self.root)

        file_menu = tk.Menu(menubar, tearoff=0)
        file_menu.add_command(label="Open", image=self.icons["open"],
                              compound="left", command=self.open_image)
        file_menu.add_command(label="Save", image=self.icons["save"],
                              compound="left", command=self.save_image)
        file_menu.add_command(label="Save As", image=self.icons["save_as"],
                              compound="left", command=self.save_image_as)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", image=self.icons["exit"],
                              compound="left", command=self.root.quit)

        edit_menu = tk.Menu(menubar, tearoff=0)
        edit_menu.add_command(label="Undo", image=self.icons["undo"],
                              compound="left", command=self.undo)
        edit_menu.add_command(label="Redo", image=self.icons["redo"],
                              compound="left", command=self.redo)

        menubar.add_cascade(label="File", menu=file_menu)
        menubar.add_cascade(label="Edit", menu=edit_menu)

        self.root.config(menu=menubar)

    # ================= LAYOUT =================

    def create_layout(self):

        # ----- LEFT PANEL (FIXED WIDTH, CENTERED CONTENT) -----
        self.left_container = tk.Frame(self.root, width=260, bg="#f0f0f0")
        self.left_container.pack(side=tk.LEFT, fill=tk.Y)
        self.left_container.pack_propagate(False)

        self.left_canvas = tk.Canvas(
            self.left_container, bg="#f0f0f0", highlightthickness=0
        )
        self.left_canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        scrollbar = tk.Scrollbar(
            self.left_container, orient=tk.VERTICAL,
            command=self.left_canvas.yview
        )
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.left_canvas.configure(yscrollcommand=scrollbar.set)

        self.left_panel = tk.Frame(self.left_canvas, bg="#f0f0f0")
        self.left_canvas.create_window(
            (130, 0), window=self.left_panel, anchor="n"
        )

        self.left_panel.bind(
            "<Configure>",
            lambda e: self.left_canvas.configure(
                scrollregion=self.left_canvas.bbox("all")
            )
        )

        # ----- WORKSPACE CONTAINER -----
        workspace = tk.Frame(self.root)
        workspace.pack(side=tk.LEFT, expand=True, fill=tk.BOTH)

        # ----- IMAGE WORKSPACE -----
        self.canvas = tk.Canvas(
            workspace, bg="#b9b9b9", highlightthickness=0
        )
        self.canvas.pack(expand=True, fill=tk.BOTH)

        # ----- STATUS BAR -----
        self.status = tk.Label(
            workspace,
            text="Ready",
            bd=1,
            relief=tk.SUNKEN,
            anchor=tk.W
        )
        self.status.pack(fill=tk.X)

        self.create_controls()


    # ================= CONTROLS =================

    def section(self, title):
        frame = tk.LabelFrame(
            self.left_panel, text=title,
            padx=10, pady=10, bg="#f0f0f0", labelanchor="n"
        )
        frame.pack(padx=10, pady=3, anchor="center")
        return frame

    def create_controls(self):

        # ---- FILTERS ----
        f = self.section("Filters")
        tk.Button(f, text="Grayscale", width=20,
                  command=self.apply_grayscale).pack(anchor="center", pady=3)
        tk.Button(f, text="Edge Detection", width=20,
                  command=self.apply_edges).pack(anchor="center", pady=3)

        # ---- ADJUSTMENTS (Blur included) ----
        a = self.section("Adjustments")

        tk.Label(a, text="Blur (1–100)", bg="#f0f0f0").pack(anchor="center")
        self.blur_slider = tk.Scale(
            a, from_=1, to=100, orient=tk.HORIZONTAL,
            command=self.preview_blur
        )
        self.blur_slider.pack(anchor="center")
        tk.Button(a, text="Apply Blur", width=20,
                  command=self.apply_blur).pack(anchor="center", pady=3)

        tk.Label(a, text="Brightness", bg="#f0f0f0").pack(anchor="center")
        self.brightness_slider = tk.Scale(
            a, from_=-100, to=100, orient=tk.HORIZONTAL,
            command=self.preview_brightness
        )
        self.brightness_slider.pack(anchor="center")
        tk.Button(a, text="Apply Brightness", width=20,
                  command=self.apply_brightness).pack(anchor="center", pady=3)

        tk.Label(a, text="Contrast", bg="#f0f0f0").pack(anchor="center")
        self.contrast_slider = tk.Scale(
            a, from_=1, to=100, orient=tk.HORIZONTAL,
            command=self.preview_contrast
        )
        self.contrast_slider.set(10)
        self.contrast_slider.pack(anchor="center")
        tk.Button(a, text="Apply Contrast", width=20,
                  command=self.apply_contrast).pack(anchor="center", pady=3)

        tk.Button(a, text="Reset Preview", width=20,
                  command=self.reset_preview).pack(anchor="center", pady=4)

        # ---- TRANSFORM ----
        t = self.section("Transform")
        tk.Button(t, text="Rotate 90°", width=20,
                  command=lambda: self.apply_rotate(90)).pack(anchor="center")
        tk.Button(t, text="Rotate 180°", width=20,
                  command=lambda: self.apply_rotate(180)).pack(anchor="center")
        tk.Button(t, text="Rotate 270°", width=20,
                  command=lambda: self.apply_rotate(270)).pack(anchor="center")
        tk.Button(t, text="Flip Horizontal", width=20,
                  command=lambda: self.apply_flip("horizontal")).pack(anchor="center")
        tk.Button(t, text="Flip Vertical", width=20,
                  command=lambda: self.apply_flip("vertical")).pack(anchor="center")

        # ---- RESIZE ----
        r = self.section("Resize")
        self.width_entry = tk.Entry(r, width=10)
        self.width_entry.insert(0, "400")
        self.width_entry.pack(anchor="center", pady=2)

        self.height_entry = tk.Entry(r, width=10)
        self.height_entry.insert(0, "300")
        self.height_entry.pack(anchor="center", pady=2)

        tk.Button(r, text="Apply Resize", width=20,
                  command=self.apply_resize).pack(anchor="center", pady=4)

    # ================= PREVIEW =================

    def preview_blur(self, value):
        if self.original_image is None:
            return
        kernel = (int(value) * 2) + 1
        self.preview_image = self.processor.blur(self.original_image, kernel)
        self.display_image(self.preview_image)

    def preview_brightness(self, value):
        if self.original_image is None:
            return
        self.preview_image = self.processor.adjust_brightness(
            self.original_image, int(value)
        )
        self.display_image(self.preview_image)

    def preview_contrast(self, value):
        if self.original_image is None:
            return
        alpha = int(value) / 50.0
        self.preview_image = self.processor.adjust_contrast(
            self.original_image, alpha
        )
        self.display_image(self.preview_image)

    # ================= APPLY =================

    def commit_preview(self):
        self.manager.commit(self.preview_image)
        self.original_image = self.preview_image
        self.preview_image = None
        self.display_image(self.original_image)
        self.update_status()

    def apply_blur(self): self.commit_preview()
    def apply_brightness(self): self.commit_preview()
    def apply_contrast(self): self.commit_preview()

    def apply_grayscale(self):
        img = self.processor.to_grayscale(self.original_image)
        self.manager.commit(img)
        self.original_image = img
        self.display_image(img)
        self.update_status()

    def apply_edges(self):
        img = self.processor.edge_detection(self.original_image)
        self.manager.commit(img)
        self.original_image = img
        self.display_image(img)
        self.update_status()

    def apply_rotate(self, angle):
        img = self.processor.rotate(self.original_image, angle)
        self.manager.commit(img)
        self.original_image = img
        self.display_image(img)
        self.update_status()

    def apply_flip(self, direction):
        img = self.processor.flip(self.original_image, direction)
        self.manager.commit(img)
        self.original_image = img
        self.display_image(img)
        self.update_status()

    def apply_resize(self):
        try:
            w = int(self.width_entry.get())
            h = int(self.height_entry.get())
            img = self.processor.resize(self.original_image, w, h)
            self.manager.commit(img)
            self.original_image = img
            self.display_image(img)
            self.update_status()
        except ValueError:
            messagebox.showerror("Error", "Width and height must be numbers")

    # ================= FILE =================

    def open_image(self):
        path = filedialog.askopenfilename(
            filetypes=[("Images", "*.jpg *.png *.bmp")]
        )
        if path:
            img = self.manager.load_image(path)
            self.original_image = img
            self.display_image(img)
            self.update_status()

    def save_image(self):
        if self.original_image is None:
            return
        os.makedirs("outputs", exist_ok=True)
        path = os.path.join("outputs", "edited_image.jpg")
        self.manager.save_image(path)
        messagebox.showinfo("Saved", f"Image saved to:\n{path}")

    def save_image_as(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".jpg",
            filetypes=[("Images", "*.jpg *.png *.bmp")]
        )
        if path:
            self.manager.save_image(path)
            messagebox.showinfo("Saved", f"Image saved to:\n{path}")

    # ================= UNDO / REDO =================

    def undo(self):
        img = self.manager.undo()
        if img is not None:
            self.original_image = img
            self.display_image(img)
            self.update_status()

    def redo(self):
        img = self.manager.redo()
        if img is not None:
            self.original_image = img
            self.display_image(img)
            self.update_status()

    # ================= DISPLAY =================

    def display_image(self, image):
        self.canvas.delete("all")

        if len(image.shape) == 2:
            image = cv2.cvtColor(image, cv2.COLOR_GRAY2RGB)
        else:
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        img = Image.fromarray(image)
        img.thumbnail((1000, 700))
        self.tk_img = ImageTk.PhotoImage(img)

        self.canvas.create_image(
            self.canvas.winfo_width() // 2,
            self.canvas.winfo_height() // 2,
            image=self.tk_img,
            anchor=tk.CENTER
        )

    def update_status(self):
        self.status.config(text=self.manager.get_info())

    def reset_preview(self):
        if self.original_image is not None:
            self.display_image(self.original_image)

    def bind_shortcuts(self):
        self.root.bind("<Control-z>", lambda e: self.undo())
        self.root.bind("<Control-y>", lambda e: self.redo())
        self.root.bind("<Control-s>", lambda e: self.save_image())
