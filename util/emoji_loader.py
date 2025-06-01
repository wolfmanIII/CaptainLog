import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
import os

class EmojiLoader:
    def __init__(self, folder_path, size=32):
        self.folder_path = folder_path
        self.size = size
        self.emoji_files = [
            ("1f600.png", "Smile"),    # 😀
            ("1f680.png", "Rocket"),   # 🚀
            ("2708.png",  "Airplane")  # ✈️
        ]
        self.images = {}
        self.load_images()

    def load_images(self):
        for i, (filename, _) in enumerate(self.emoji_files):
            path = os.path.join(self.folder_path, filename)
            img = Image.open(path).resize((self.size, self.size), Image.ANTIALIAS)
            self.images[i] = ImageTk.PhotoImage(img)

    def get_image(self, index):
        return self.images.get(index, None)

    def get_description(self, index):
        if 0 <= index < len(self.emoji_files):
            return self.emoji_files[index][1]
        return ""