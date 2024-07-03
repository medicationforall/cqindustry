import cadquery as cq
from cadqueryhelper import Base
from cqspoolterrain.pipe import straight
from . import Ring, ChipCan, CanPlatform

class CanTower(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.render_can:bool = False
        self.can_height:float = 122
        self.can_diameter:float = 66
        self.cut_padding:float = .5
        self.ring_width:float = 4.5
        self.platform_height:float = 20
        self.platform_ladder_extends:float = 10
        
        #blueprints
        self.bp_ring = Ring()
        self.bp_ring.height = 10
        self.bp_ring.ladder_width = 5
        
        self.bp_can = ChipCan()
        self.bp_chip_cut = ChipCan()
        
        self.bp_platform = CanPlatform()
        
        #shapes
        self.pipe:cq.Workplane|None = None
        
    def make(self, parent=None):
        super().make(parent)
        
        self.bp_ring.diameter = self.can_diameter + (self.ring_width*2)
        self.bp_ring.cut_diameter = self.can_diameter + self.cut_padding
        self.bp_ring.ladder_height = self.can_height - self.platform_height/2
        self.bp_ring.make()
        
        self.bp_can.height = self.can_height
        self.bp_can.diameter = self.can_diameter
        self.bp_can.make()
        
        self.bp_chip_cut.height = self.can_height
        self.bp_chip_cut.diameter = self.can_diameter + self.cut_padding
        self.bp_chip_cut.make()
        
        self.bp_platform.diameter = self.can_diameter + (self.ring_width*2)
        self.bp_platform.cut_diameter = self.can_diameter + self.cut_padding
        self.bp_platform.height = self.platform_height
        self.bp_platform.cut_height = self.platform_height/2
        self.bp_platform.ladder_height = self.platform_height + self.platform_ladder_extends
        self.bp_platform.make()
        
        self.pipe = straight(render_hollow=False, render_through_hole = False)
        
    def build(self):
        ring = self.bp_ring.build()
        soda_can = self.bp_can.build()
        soda_can_cut = self.bp_chip_cut.build()
        platform = self.bp_platform.build()

        scene = (
            cq.Workplane("XY")
            .union(self.pipe)
            .cut(soda_can_cut.translate((0,0,self.bp_can.height /2)))
            .union(ring)
            #.union(self.bp_ring.cut_ladders)
            .add(platform.translate((0,0,self.bp_can.height))) 
        )

        if self.render_can:
            scene.add(soda_can.translate((0,0,self.bp_can.height /2)))
        return scene