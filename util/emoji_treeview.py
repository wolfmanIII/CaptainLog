import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageDraw, ImageFont, ImageTk
import sys
import os

def get_emoji_font_path():
    if sys.platform == "win32":
        possible_paths = [
            "C:\\Windows\\Fonts\\seguiemj.ttf",
            "C:\\Windows\\Fonts\\seguisym.ttf"
        ]
    elif sys.platform == "darwin":
        possible_paths = [
            "/System/Library/Fonts/Apple Color Emoji.ttc",
            "/System/Library/Fonts/Apple Color Emoji.ttf"
        ]
    else:
        possible_paths = [
            "/usr/share/fonts/truetype/noto/NotoColorEmoji.ttf",
            "/usr/share/fonts/truetype/emoji/NotoColorEmoji.ttf"
        ]

    for path in possible_paths:
        if os.path.isfile(path):
            return path
    raise FileNotFoundError("Font emoji non trovato nel sistema")

def emoji_to_image(emoji_char, size=32, font_path=None):
    image = Image.new("RGBA", (size, size), (255, 255, 255, 0))
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(font_path, size)

    # usa textbbox per ottenere dimensioni testo
    bbox = draw.textbbox((0, 0), emoji_char, font=font)
    w = bbox[2] - bbox[0]
    h = bbox[3] - bbox[1]

    draw.text(((size - w) / 2, (size - h) / 2), emoji_char, font=font, fill=(0, 0, 0))
    return image

root = tk.Tk()
root.title("Treeview con emoji generate dinamicamente")

try:
    font_path = get_emoji_font_path()
except FileNotFoundError as e:
    print(e)
    font_path = None

if not font_path:
    label = tk.Label(root, text="Font emoji non trovato nel sistema.")
    label.pack()
    root.mainloop()
    exit()

tree = ttk.Treeview(root, columns=("Descrizione",))
tree.heading("#0", text="Emoji")
tree.heading("Descrizione", text="Descrizione")
tree.column("#0", width=40, anchor="center")
tree.column("Descrizione", width=150)

# Lista di emoji + descrizioni
emoji_list = [
    ("😀", "Sorriso"),
    ("🚀", "Razzo"),
    ("👍", "Pollice su"),
    ("🐍", "Serpente"),
    ("🍕", "Pizza")
]

# Memorizza i riferimenti alle immagini per non perderle
images = {}

for i, (em, desc) in enumerate(emoji_list):
    img = emoji_to_image(em, size=12, font_path=font_path)
    tk_img = ImageTk.PhotoImage(img)
    images[i] = tk_img  # salva riferimento!
    tree.insert("", "end", text="", image=tk_img, values=(desc,))

tree.pack(padx=10, pady=10)

root.mainloop()