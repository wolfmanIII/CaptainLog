import numpy as np
from moviepy import ImageClip, ColorClip, CompositeVideoClip
from PIL import Image, ImageDraw, ImageFont

# Parametri video
W, H = 1280, 720
duration = 40
scroll_speed = 40

# Testo dell'introduzione
intro_text = """Anno 1105.
Nelle remote Spinward Marches,
una tensione crescente minaccia
i mondi di confine dell’Impero.

Misteriosi attentati falliti hanno
colpito la nobile Casa Norris,
mentre corporazioni rivali e
intrighi politici agitano il settore.

A Flammarion, alla vigilia della
festa di Capodanno Imperiale,
voci di rovine degli Antichi
riemergono dall’ombra del passato...

Un nuovo viaggio sta per iniziare...
"""

# Font
font_size = 40
try:
    font = ImageFont.truetype("DejaVuSans.ttf", font_size)
except:
    font = ImageFont.load_default()

# Calcolo altezza linea
dummy_img = Image.new("RGB", (10,10))
draw_dummy = ImageDraw.Draw(dummy_img)
bbox = draw_dummy.textbbox((0,0), "Ay", font=font)
line_height = bbox[3] - bbox[1] + 5

# Creazione immagine testo (aggiungiamo H per far scorrere tutto)
lines = intro_text.split("\n")
img_height = line_height * len(lines) + H
img_width = int(W*0.8)

img = Image.new("RGBA", (img_width, img_height), (0,0,0,0))
draw = ImageDraw.Draw(img)

# Scriviamo il testo centrato
y = 0
for line in lines:
    bbox = draw.textbbox((0,0), line, font=font)
    w = bbox[2] - bbox[0]
    draw.text(((img_width - w)/2, y), line, font=font, fill="yellow")
    y += line_height

# Convertiamo in array NumPy
img_np = np.array(img)
crawl = ImageClip(img_np).with_duration(duration)

# Movimento verticale sicuro
def move_text(t):
    y = H - scroll_speed*t  # parte sotto lo schermo
    return ('center', y)

scrolling = crawl.with_position(move_text)

# Sfondo nero
background = ColorClip(size=(W,H), color=(0,0,0)).with_duration(duration)

# Composizione finale
video = CompositeVideoClip([background, scrolling]).with_duration(duration)

# Salvataggio
video.write_videofile("traveller_intro.mp4", fps=24, codec="libx264")
