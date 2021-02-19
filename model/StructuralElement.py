class StructuralElement:
    """Super class to all structural elements"""
    def __init__(self, showbase):
        self.render = showbase.render

    def draw(self):
        pass