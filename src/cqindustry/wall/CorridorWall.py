import cadquery as cq
from cqterrain.wall import BaseWall
from cadqueryhelper.shape import trapezoid

class CorridorWall(BaseWall):
    def __init__(self):
        super().__init__()
        #parameters
        self.width:float = 12
        self.inner_width:float = 4
        self.inner_height:float = 25
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.wall:cq.Workplane|None = None
        self.wall_cut:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_wall(self):
        length = self.length
        width = self.width
        height = self.height
        wall = cq.Workplane("XY").box(length,width,height)
        self.wall = wall
        
    def make_wall_cut(self):
        length = self.length
        height = self.height
        width = self.width - self.inner_width
        inner_height = self.inner_height
        wall_cut = trapezoid(
            length = length,
            width = height,
            height = width,
            top_width = inner_height
        ).rotate((0,1,0),(0,0,0),-90).rotate((0,0,1),(0,0,0),-90)
        
        y_translate = self.inner_width /2
        self.wall_cut = wall_cut.translate((0,-y_translate,0))

    def make(self):
        super().make()
        self.make_outline()
        self.make_wall()
        self.make_wall_cut()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
            
        if self.wall_cut:
            part = part.cut(self.wall_cut)
        
        return part