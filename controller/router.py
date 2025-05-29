class Router:
    
    def __init__(self, container):
        self.container = container
        self.views = {}

    def add_view(self, name, view_cls):
        frame = view_cls(self.container, self)
        self.views[name] = frame
        frame.grid(row=0, column=0, sticky="nsew")

    def navigate(self, name):
        frame = self.views[name]
        frame.tkraise()

    def get_view(self, name):
        return self.views.get(name)