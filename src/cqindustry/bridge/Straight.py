import cadquery as cq
import math
from cqterrain.bridge import BaseStraight
from cqterrain.tile import plain
from cadqueryhelper import shape, grid

class Straight(BaseStraight):
    def __init__(self):
        super().__init__()
        #parameters
        self.padding:float = 4

        self.render_floor:bool = True
        self.floor_height:float = 1
        self.floor_tile_size:float = 12
        self.floor_tile_padding:float = 2
        self.floor_pading:float = 2
        self.corner_chamfer:float = 10

        self.base_top_margin:float = 10
        self.base_side_margin:float = 10
        self.base_fillet:float = 8
        
        self.base_inset_distance_height:float = 2
        self.base_inset_distance:float = 2
        self.base_inset_depth:float = 2
        self.base_inset_fillet:float = 9
        
    def make_base_cut(self):
        base_cut = (
            cq.Workplane("XY")
            .box(
                self.length-self.base_side_margin*2,
                self.width,
                self.height - self.base_top_margin,
            )
            .faces("Z")
            .edges("Y")
            .fillet(self.base_fillet)
        )
        
        self.straight = (
            self.straight
            .cut(base_cut.translate((0,0,-self.base_top_margin/2))) #type:ignore
        )
        
    def make_base_inset(self):
        base_inset = (
            cq.Workplane("XY")
            .box(
                self.length-self.base_side_margin*2+self.base_inset_distance*2,
                self.base_inset_depth,
                self.height - self.base_top_margin+self.base_inset_distance_height,
            )
            .faces("Z")
            .edges("Y")
            .fillet(self.base_inset_fillet)
        )
        
        self.straight = (
            self.straight
            .cut(base_inset.translate(( #type:ignore
                0,
                self.width/2-self.base_inset_depth/2,
                -self.base_top_margin/2+self.base_inset_distance_height/2
            )))
            .cut(base_inset.translate((
                0,
                -self.width/2+self.base_inset_depth/2,
                -self.base_top_margin/2+self.base_inset_distance_height/2
            )))
        )
        
        
    def __make_floor_tiles(self):
        #tile
        diamond:cq.Workplane = shape.diamond(
            self.floor_tile_size,
            self.floor_tile_size,
            self.floor_height
        ).faces("-Z").chamfer(.4)


        x_count:int = math.floor((self.length-self.padding*2) / (self.floor_tile_size+self.floor_tile_padding))
        y_count:int = math.floor((self.width-self.padding*2) / ((self.floor_tile_size+self.floor_tile_padding)/2))

        # make tiles
        diamonds:cq.Workplane = grid.make_grid(
            diamond,
            [self.floor_tile_size+self.floor_tile_padding, (self.floor_tile_size+self.floor_tile_padding)/2],
            rows = x_count+2,
            columns = y_count+2,
            odd_col_push = [(self.floor_tile_size+self.floor_tile_padding)/2,0]
        )

        outline = (
            cq.Workplane("XY")
            .box(
                self.length - self.padding*2,
                self.width - self.padding*2,
                self.height/2
            )
        )

        if self.corner_chamfer:
            outline = (
                outline
                .faces("X or -X")
                .edges("Z")
                .chamfer(self.corner_chamfer)
            )

        outline = outline.translate((0,0,self.height/2))

        # doing a union here to merge all of the separate tile entities into one shape prior to the intersect operation.
        floor_tiles:cq.Workplane = cq.Workplane("XY").union(diamonds.translate((
            0,
            0,
            self.floor_height/2+self.height/2
        )))

        self.floor_tiles = outline.intersect(floor_tiles).translate((0,0,-1))
        
    def make(self, parent=None):
        super().make(parent)
        if self.straight:
            self.make_base_cut()
            self.make_base_inset()

            if self.render_floor:
                self.__make_floor_tiles()
            
        else:
            raise Exception("Unable to resolve straight bridge segment")

        
    def build(self):
        super().build()
        if self.straight:
            scene = (
                cq.Workplane("XY")
                .add(self.straight)
            )

            if self.render_floor and self.floor_tiles:
                scene = scene.cut(self.floor_tiles)

            return scene
        else:
            raise Exception("Unable to resolve straight bridge segment")
