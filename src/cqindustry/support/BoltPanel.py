from cqterrain.tile import bolt_panel
from . import Segmented

class BoltPanel(Segmented):
    def __init__(self):
        super().__init__()
        self.chamfer:float = 0.5
        self.radius_outer:float = 1
        self.radius_internal:float = 0.5
        self.cut_height:float = 0.5
        self.padding:float = 2
        
    def make_tile(self):
        length = self.calculate_internal_length()
        segment_height = self.calculate_segment_height()
        tile_width = self.calculate_tile_width()
        
        self.tile = bolt_panel(
            length = length, 
            width = segment_height, 
            height = tile_width, 
            chamfer = self.chamfer, 
            radius_outer = self.radius_outer,
            radius_internal = self.radius_internal,
            cut_height = self.cut_height,
            padding = self.padding
        )