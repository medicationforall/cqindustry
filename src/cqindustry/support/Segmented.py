import cadquery as cq
from . import Basic

class Segmented(Basic):
    def __init__(self):
        super().__init__()
        #parameters
        self.segments:int = 5
        self.side_length:float = 2
        self.height_margin:float = 3
        self.tile_depth:float = 1
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.internal_outline:cq.Workplane|None = None
        self.sides:cq.Workplane|None = None
        self.tile:cq.Workplane|None = None 
        self.tiles:cq.Workplane|None = None
        
    
    def calculate_internal_length(self):
        return self.length - self.side_length*2
    
    
    def calculate_internal_height(self):
        return self.height - self.height_margin*2
    
    
    def calculate_segment_height(self):
        return self.calculate_internal_height() / self.segments
    
    def calculate_tile_width(self):
        return self.width - self.tile_depth
    
    
    def make_internal_outline(self):
        height = self.calculate_internal_height()
        length = self.calculate_internal_length()
        self.internal_outline = cq.Workplane("XY").box(length, self.width, height)
        
        
    def make_sides(self):
        length = self.calculate_internal_length()
        internal_cut = cq.Workplane("XY").box(length, self.width, self.height)
        self.sides = self.outline.cut(internal_cut)
    
        
    def make_tile(self):
        length = self.calculate_internal_length()
        segment_height = self.calculate_segment_height()
        tile_width = self.calculate_tile_width()
        
        self.tile = (
            cq.Workplane("XY")
            .box(length, segment_height, tile_width)
            #.rotate((1,0,0),(0,0,0),-90)
        )
        
    def add_tile(self):
        count = 0
        def adder_function(loc)->cq.Shape:
            #nonlocal count
            #count += 1
            return self.tile.val().located(loc) 
        return adder_function
        
    def make_tiles(self):
        length = self.calculate_internal_length()
        height = self.calculate_segment_height()
        
        tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = length, 
                ySpacing = height,
                xCount = 1, 
                yCount= self.segments, 
                center = True)
            .eachpoint(self.add_tile())
        ).rotate((1,0,0),(0,0,0),-90)
        
        self.tiles = tiles
        
        
    def make(self, parent=None):
        super().make(parent)
        self.make_internal_outline()
        self.make_sides()
        self.make_tile()
        self.make_tiles()
        
    def build(self)->cq.Workplane:
        super().build()
        scene = cq.Workplane()
        
        if self.sides:
            print('building sides')
            scene = scene.add(self.sides)
            
        if self.tiles:
            scene = scene.union(self.tiles.translate((0,self.tile_depth/2,0)))

        return scene