class Router:

    def __init__(self, container):
        self.container = container
        self.view_classes = {}  # Mapping nome -> classe della view
        self.views = {}         # Mapping nome -> istanza (opzionale)

    def add_view(self, name, view_cls):
        self.view_classes[name] = view_cls  # Non creiamo subito l'istanza

    def navigate(self, name, **kwargs):
        # Distruggiamo la view precedente (se presente)
        if name in self.views:
            self.views[name].destroy()

        view_cls = self.view_classes.get(name)
        if view_cls is None:
            raise ValueError(f"View '{name}' non registrata.")

        frame = view_cls(self.container, self, **kwargs)
        self.views[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")
        frame.tkraise()

    def get_view(self, name):
        return self.views.get(name)