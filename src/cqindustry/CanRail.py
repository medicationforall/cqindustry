import cadquery as cq
from cadqueryhelper import Base
from . import CanPlatform

class CanRail(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.parent:CanPlatform|None = None
        self.height = 20
        self.rail_width = 3
        self.rail_height = 2
        
        self.support_count = 6
        self.support_length = 2.5
        self.support_width = 2
        self.support_height = 25
        
        #shapes
        self.rail = None
        self.support = None
        self.supports = None
        self.cut_rail = None
        
    def __make_rail(self):
        if self.parent:
            rail_outline = cq.Workplane("XY").cylinder(self.rail_height, self.parent.diameter/2+self.rail_width)
            rail_cut = cq.Workplane("XY").cylinder(self.rail_height, self.parent.diameter/2)
            self.rail = rail_outline.cut(rail_cut)
        
    def __make_cut_rail(self):
        if self.parent:
            cut_rail = cq.Workplane("XY").box(self.parent.ladder_length, self.parent.diameter+(self.rail_width*2) , self.height)
            self.cut_rail = cut_rail
        
    def __make_support(self):
        support = cq.Workplane("XY").box(
            self.support_length,
            self.support_width,
            self.support_height
        )
        self.support = support
        
    def __make_supports(self):
        def add_support(loc: cq.Location)->cq.Shape:
            return self.support.val().located(loc) #type: ignore
        
        if self.parent:
            supports = (
                cq.Workplane("XY")
                .polarArray(
                    radius = self.parent.diameter/2, 
                    startAngle = 0, 
                    angle = 360, 
                    count = self.support_count,
                    fill = True,
                    rotate = True
                )
                .eachpoint(callback = add_support)
            )
            self.supports = supports 
        
    def make(self, parent = None):
        super().make(parent)
        self.__make_rail()
        self.__make_cut_rail()
        self.__make_support()
        self.__make_supports()
        
    def build(self) -> cq.Workplane:
        super().build()
        if self.parent and self.rail and self.cut_rail and self.supports:
            parent_platform = self.parent.build()
            scene = (
                cq.Workplane("XY")
                .union(self.rail.translate((0,0,self.height-self.rail_height/2)))
                .union(self.rail.translate((0,0,self.height/2)))
                .cut(self.cut_rail.translate((0,0,self.height/2)))
                .union(self.supports.translate((0,0,self.height-self.support_height/2)))
            
            ).translate((0,0,self.parent.height/2)).cut(parent_platform)
            return scene
        else:
            raise Exception("Unabel to build CanRail")