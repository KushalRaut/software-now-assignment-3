import tkinter as tk
from tkinter import filedialog, messagebox

class ImageEditorUI:
    def __init__(self, root):
        self.root = root
        self.root.title("HIT137 - Image Processing App")
        self.root.geometry("1000x650")

        # ===== MENU BAR =====
        self.menu_bar = tk.Menu(self.root)

        # File Menu
        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.file_menu.add_command(label="Open")
        self.file_menu.add_command(label="Save")
        self.file_menu.add_command(label="Save As")
        self.file_menu.add_separator()
        self.file_menu.add_command(label="Exit", command=self.root.quit)
        self.menu_bar.add_cascade(label="File", menu=self.file_menu)

        # Edit Menu
        self.edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.edit_menu.add_command(label="Undo")
        self.edit_menu.add_command(label="Redo")
        self.menu_bar.add_cascade(label="Edit", menu=self.edit_menu)

        self.root.config(menu=self.menu_bar)

        # ===== MAIN LAYOUT =====
        self.main_frame = tk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # ===== CONTROL PANEL (LEFT SIDEBAR) =====
        self.control_panel = tk.Frame(self.main_frame, width=250, bg="#f0f0f0", relief=tk.RIDGE, bd=2)
        self.control_panel.pack(side=tk.LEFT, fill=tk.Y)

        tk.Label(self.control_panel, text="Filters & Effects", font=("Arial", 12, "bold"), bg="#f0f0f0").pack(pady=10)

        buttons = [
            "Grayscale",
            "Blur",
            "Edge Detection",
            "Brightness +",
            "Brightness -",
            "Contrast +",
            "Contrast -",
            "Rotate 90°",
            "Rotate 180°",
            "Rotate 270°",
            "Flip Horizontal",
            "Flip Vertical",
            "Resize"
        ]

        for b in buttons:
            btn = tk.Button(self.control_panel, text=b, width=20)
            btn.pack(pady=2)

        # ===== IMAGE DISPLAY AREA (CENTER) =====
        self.display_frame = tk.Frame(self.main_frame, bg="white", relief=tk.SUNKEN, bd=2)
        self.display_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.canvas = tk.Canvas(self.display_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True)

        # ===== STATUS BAR =====
        self.status_bar = tk.Label(self.root, text="No image loaded", bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)


if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditorUI(root)
    root.mainloop()
