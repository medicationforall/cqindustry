import cadquery as cq
from cqterrain.tile import bolt_panel
from cadqueryhelper.shape import rail
from . import Segmented

class Strut(Segmented):
    def __init__(self):
        super().__init__()
        self.strut_width:float = 1.5
        
    def make_tile(self):
        length = self.calculate_internal_length()
        segment_height = self.calculate_segment_height()
        tile_width = self.calculate_tile_width()
        
        tile = rail(
            length=length, 
            width=tile_width, 
            height=segment_height, 
            inner_height=self.strut_width
        ).rotate((1,0,0),(0,0,0),-90)
        
        #outline = cq.Workplane("XY").box(
        #    length=length, 
        #    width=segment_height, 
        #    height=tile_width-2
        #)
        
        self.tile = tile
        
    def add_tile(self):
        count = 0
        tile = self.tile
        tile_rotated = self.tile.rotate((0,1,0),(0,0,0),180)
        def adder_function(loc)->cq.Shape:
            nonlocal count
            nonlocal tile
            nonlocal tile_rotated
            
            count += 1
            l_tile = tile
            
            if count % 2 == 1:
                l_tile = tile_rotated
            
            return l_tile.val().located(loc) 
        return adder_function