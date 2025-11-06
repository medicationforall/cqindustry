import cadquery as cq
from cadqueryhelper import Base


class Basic(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 25
        self.width:float = 5
        self.height:float = 50
        
        #shapes
        self.outline:cq.Workplane|None = None
    
    def make_outline(self):
        outline = cq.Workplane("XY").box(self.length, self.width, self.height)
        self.outline = outline
        
        
    def make(self, parent=None):
        super().make(parent)
        self.make_outline()
        
        
    def build_outline(self)->cq.Workplane:
        super().build()
        scene = cq.Workplane()
        
        scene = scene.union(self.outline)
        
        return scene
        
        
    def build(self)->cq.Workplane:
        super().build()
        scene = cq.Workplane()
        scene = scene.union(self.outline)
        
        return scene