import os
from PIL import Image, ImageTk

class EmojiCache:
    _instance = None
    _cache = {}

    def __new__(cls, base_path="resource/twemoji/72x72", size=14):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.base_path = base_path
            cls._instance.size = size
            cls._instance._load_emojis()
        elif cls._instance.base_path != base_path or cls._instance.size != size:
            cls._instance.base_path = base_path
            cls._instance.size = size
            cls._instance._cache.clear()
            cls._instance._load_emojis()
        return cls._instance

    def _load_emojis(self):
        for file in os.listdir(self.base_path):
            if file.endswith(".png"):
                full_path = os.path.join(self.base_path, file)
                try:
                    img = Image.open(full_path).resize((self.size, self.size), Image.Resampling.LANCZOS)
                    tk_img = ImageTk.PhotoImage(img)
                    self._cache[file] = tk_img
                except Exception as e:
                    print(f"Errore caricando {file}: {e}")

    def get(self, filename):
        """Restituisce un'immagine emoji (ImageTk.PhotoImage) o None."""
        return self._cache.get(filename)

    def all(self):
        """Restituisce tutte le emoji caricate."""
        return self._cache.copy()
