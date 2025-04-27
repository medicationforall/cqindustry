import cadquery as cq
import math
from cadqueryhelper import Base
from cqterrain import tile, Ladder
from typing import Callable

class CanPlatform(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.height:float = 20
        self.diameter:float = 75
        self.cut_diameter:float = 66.5
        self.cut_height:float = 10
        self.tile_length:float = 15
        self.tile_width:float = 15
        self.tile_height:float = 3
        self.tile_method:Callable[[float,float,float],cq.Workplane] = tile.bolt_panel

        self.ladder_length:float = 25
        self.ladder_width:float = 5
        self.ladder_height:float = 30
        self.ladder_cut_padding:float = 1
        self.ladder_cut_chamfer:float = 2

        #blueprints
        self.bp_ladder:Ladder = Ladder()

        #shapes
        self.platform:cq.Workplane|None = None
        self.cut_cylinder:cq.Workplane|None = None
        self.tile_intersect:cq.Workplane|None = None
        self.tiles:cq.Workplane|None = None
        self.cut_ladders:cq.Workplane|None = None
        
    def _make_tile(self):
        self.tile = self.tile_method(self.tile_length, self.tile_width, self.tile_height)
    
    def _make_tiles(self):
        def add_tile(loc: cq.Location) -> cq.Shape:
            return self.tile.val().located(loc) #type: ignore
        
        x_count = math.floor(self.diameter/self.tile_length)
        y_count = math.floor(self.diameter/self.tile_width) 

        self.tiles = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.tile_length, 
                ySpacing = self.tile_width,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(add_tile)
        )

    def __make_cut_ladders(self):
        x_translate = self.cut_diameter/2+self.ladder_length/2+self.ladder_cut_padding
        cut_ladder = (
            cq.Workplane("XY")
            .box(self.ladder_length,self.ladder_length,self.height)
            .faces("X or -X")
            .edges("Z")
            .chamfer(self.ladder_cut_chamfer)
            .translate((
                0,
                x_translate,
                0
            ))
        )

        cut_ladders = (
            cq.Workplane("XY")
            .union(cut_ladder)
            .union(cut_ladder.rotate((0,0,1),(0,0,0),180))
        )
        self.cut_ladders = cut_ladders

    def _make_ladder(self):
        self.bp_ladder.length = self.ladder_length
        self.bp_ladder.width = self.ladder_width
        self.bp_ladder.height = self.ladder_height
        self.bp_ladder.make()

        if self.bp_ladder.rungs:
            self.bp_ladder.rungs = self.bp_ladder.rungs.translate((0,self.ladder_width/4,0))
    
    def make(self, parent=None):
        super().make(parent)
        self.platform = cq.Workplane("XY").cylinder(self.height - self.tile_height, self.diameter/2) 
        self.tile_intersect = cq.Workplane("XY").cylinder(self.tile_height, self.diameter/2)
        self.cut_cylinder = cq.Workplane("XY").cylinder(self.cut_height, self.cut_diameter/2)
        self._make_tile()
        self._make_tiles()
        self.__make_cut_ladders()
        self._make_ladder()

    def build_ladders(self) -> cq.Workplane:
        ladder = self.bp_ladder.build().translate((
            0,
            self.cut_diameter/2+.6,
            -self.height/2+self.ladder_height/2
        ))

        if self.cut_cylinder:
            ladder = ladder.cut(self.cut_cylinder)

        ladders = (
            cq.Workplane()
            .union(ladder)
            .union(ladder.rotate((0,0,1),(0,0,0),180))
        )

        return ladders
    
    def __validate_build(self):
            missing = ""
            if not self.tiles:
                missing='tiles'
            elif not self.tile_intersect:
                missing='tile intersect'
            elif not self.cut_ladders:
                missing='cut_ladders'
            elif not self.platform:
                missing='platform'
            elif not self.cut_cylinder:
                missing='cut_cylinder'
            if missing:
                raise Exception(f'CanPlatform could not resolve one of the required build components. Missing: {missing}')
            else:
                return True

    def build(self) -> cq.Workplane:
        super().build()
        ladders = self.build_ladders()

        if self.__validate_build():
            scene = (
                cq.Workplane("XY")
                .union(self.tiles.translate((0,0,self.height/2-self.tile_height/2))) # type: ignore
                .intersect(self.tile_intersect.translate((0,0,self.height/2-self.tile_height/2))) # type: ignore
                .add(self.platform.translate((0,0,-self.tile_height/2))) # type: ignore
                .cut(self.cut_ladders) # type: ignore
                .cut(self.cut_cylinder.translate((0,0,-1*(self.height/2)+(self.cut_height/2)))) # type: ignore
                .union(ladders)
            )
            return scene
        else:
            raise Exception('CanPlatform Build validation failed')
