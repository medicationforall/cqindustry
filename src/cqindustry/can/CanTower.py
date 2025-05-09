import cadquery as cq
from cadqueryhelper import Base
from cqterrain.pipe import straight
from ..chip import ChipCan, Ring
from . import CanPlatform, CanRail

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
        self.pipe_length:float = 75
        
        #blueprints
        self.bp_ring:Ring = Ring()
        self.bp_ring.height = 10
        self.bp_ring.ladder_width = 5
        
        self.bp_can:ChipCan = ChipCan()
        self.bp_chip_cut:ChipCan = ChipCan()
        
        self.bp_platform:CanPlatform = CanPlatform()
        self.bp_rail:CanRail = CanRail()
        
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
        
        self.bp_rail.make(self.bp_platform)
        
        self.pipe = straight(length = self.pipe_length, render_hollow=False, render_through_hole = False)

    def build_ring_pipe_connector(self):
        ring = self.bp_ring.build()
        soda_can_cut = self.bp_chip_cut.build()
        pipe = self.pipe

        ring_pipe = (
            cq.Workplane("XY")
            .union(self.pipe)
            .cut(soda_can_cut.translate((0,0,self.bp_can.height /2)))
            .union(ring)
        )

        return ring_pipe

    def build(self):
        soda_can = self.bp_can.build()
        platform = self.bp_platform.build()
        rail = self.bp_rail.build()
        ring = self.build_ring_pipe_connector()

        scene = (
            cq.Workplane("XY")
            .union(ring)
            .add(platform.translate((0,0,self.bp_can.height))) 
            .add(rail.translate((0,0,self.bp_can.height)))
        )

        if self.render_can:
            scene.add(soda_can.translate((0,0,self.bp_can.height /2)))
        return scene
    
    def build_plate(self):
        platform = self.bp_platform.build()
        rail = self.bp_rail.build()
        ring = self.build_ring_pipe_connector()

        scene = (
            cq.Workplane("XY")
            .union(ring)
            .add(platform.translate((0,self.can_diameter+self.ring_width+10,self.bp_platform.height/2))) 
            .add(rail.rotate((0,1,0),(0,0,0),180).translate((0,(self.can_diameter+self.ring_width+10)*2,self.bp_rail.height+(self.bp_platform.height/2))))
        )

        return scene