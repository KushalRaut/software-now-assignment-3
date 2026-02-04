# OOP Image Processing Application

A desktop application built with Python, Tkinter, and OpenCV that demonstrates Object-Oriented Programming principles and provides comprehensive image processing capabilities.

## 📋 Project Overview

This application is developed as part of HIT137 Assignment 3, showcasing:
- **Object-Oriented Programming** principles (Encapsulation, Constructors, Methods, Class Interaction)
- **GUI Development** using Tkinter
- **Image Processing** using OpenCV

## ✨ Features

### Image Processing Operations
- **Grayscale Conversion** - Convert images to black and white
- **Blur Effect** - Apply Gaussian blur with adjustable intensity
- **Edge Detection** - Canny edge detection algorithm
- **Brightness Adjustment** - Increase or decrease image brightness
- **Contrast Adjustment** - Modify image contrast levels
- **Image Rotation** - Rotate by 90°, 180°, or 270°
- **Image Flip** - Flip horizontally or vertically
- **Resize/Scale** - Adjust image dimensions

### GUI Features
- **Menu Bar** with File (Open, Save, Save As, Exit) and Edit (Undo, Redo) options
- **Image Display Area** for real-time preview
- **Control Panel** with easy-to-use buttons and sliders
- **Status Bar** showing current image information
- **File Dialog Support** for JPG, PNG, and BMP formats
- **Error Handling** with message boxes

## 🛠️ Technologies Used

- **Python 3**
- **Tkinter** – GUI development
- **OpenCV (cv2)** – Image processing
- **Pillow (PIL)** – Image rendering in GUI
- **NumPy** – Image data handling

---

## 🚀 Getting Started

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone the repository**
```bash
git clone https://github.com/mazharsnow/oop-image-editor.git
cd oop-image-editor
```

2. **Create a virtual environment**

Open terminal in VS Code and run:

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS / Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

You should see `(venv)` in your terminal prompt.

3. **Install required libraries**
```bash
pip install opencv-python pillow numpy
```

4. **Verify installation**
```bash
python -c "import cv2, PIL, numpy; print('All libraries installed successfully!')"
```

## 🎮 Usage

1. **Run the application**
```bash
python main.py
```

2. **Open an image**
   - Click `File → Open` or use the Open button
   - Select an image file (JPG, PNG, or BMP)

3. **Apply effects**
   - Use the control panel buttons to apply various effects
   - Adjust sliders for intensity-based effects (blur, brightness, contrast)
   - Preview changes in real-time

4. **Save your work**
   - Click `File → Save` to overwrite the original
   - Click `File → Save As` to save with a new name

5. **Undo/Redo**
   - Use `Edit → Undo` or `Edit → Redo` to navigate through changes

## 📁 Project Structure

```
OOP_PROJECT/
│
├── assets/
│   ├── icons/              # UI icons
│   │   ├── exit.png
│   │   ├── open.png
│   │   ├── redo.png
│   │   ├── save_as.png
│   │   ├── save.png
│   │   └── undo.png
│   └── istockphoto-183412466-612x612.jpg
│
├── outputs/                # Saved processed images
│   └── edited_image.jpg
│
├── venv/                   # Virtual environment (not tracked)
│
├── gui.py                  # GUI class implementation
├── image_manager.py        # Image management class
├── image_processor.py      # Image processing class
├── main.py                 # Main application entry point
├── github_link.txt         # GitHub repository link
└── README.md              # This file
```

## 🏗️ Architecture

### Object-Oriented Design

The application follows OOP principles with three main classes:

1. **ImageProcessor** (`image_processor.py`)
   - Handles all image processing operations
   - Encapsulates OpenCV functions
   - Methods for filters, effects, and transformations

2. **ImageManager** (`image_manager.py`)
   - Manages image state and history
   - Implements undo/redo functionality
   - Handles file I/O operations

3. **GUI** (`gui.py`)
   - Manages the Tkinter interface
   - Handles user interactions
   - Coordinates between ImageProcessor and ImageManager

### Class Interaction
```
main.py
   └── GUI
       ├── ImageManager (manages image state)
       └── ImageProcessor (processes images)
```

## 🛠️ Technologies Used

- **Python 3.x** - Core programming language
- **Tkinter** - GUI framework
- **OpenCV (cv2)** - Image processing library
- **PIL/Pillow** - Image handling and display
- **NumPy** - Numerical operations

## 📄 License

This project is created for educational purposes as part of HIT137 coursework.

## 🐛 Known Issues

- None reported

## 🔮 Future Enhancements

- Additional filters (sepia, vintage, etc.)
- Batch processing capabilities
- Image filters preview before applying
- Keyboard shortcuts for common operations
- Custom filter creation


---

**Note:** Make sure to keep your virtual environment activated when running the application. If you close the terminal, reactivate it using the appropriate command for your operating system.
