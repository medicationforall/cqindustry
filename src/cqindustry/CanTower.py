import cadquery as cq
from cadqueryhelper import Base
from cqspoolterrain.pipe import straight
from . import Ring, ChipCan

class CanTower(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.render_can = False
        
        #blueprints
        self.bp_ring = Ring()
        self.bp_ring.diameter = 75
        self.bp_ring.cut_diameter = 66.5
        self.bp_ring.height = 10
        self.bp_ring.ladder_height = 112
        self.bp_ring.ladder_width = 5
        
        self.bp_can = ChipCan()
        self.bp_can.height = 122
        self.bp_can.diameter = 66
        
        self.bp_chip_cut = ChipCan()
        self.bp_chip_cut.height = 122
        self.bp_chip_cut.diameter = 66.5

        #shapes
        self.pipe = None
        
    def make(self, parent=None):
        super().make(parent)
        self.bp_ring.make()
        self.bp_can.make()
        self.bp_chip_cut.make()
        self.pipe = straight(render_hollow=False, render_through_hole = False)
        
        
    def build(self):
        ring = self.bp_ring.build()
        soda_can = self.bp_can.build()
        soda_can_cut = self.bp_chip_cut.build()

        scene = (
            cq.Workplane("XY")
            .union(self.pipe)
            .cut(soda_can_cut.translate((0,0,self.bp_can.height /2)))
            .union(ring)
            #.union(self.bp_ring.cut_ladders)
            
        )

        if self.render_can:
            scene.add(soda_can.translate((0,0,self.bp_can.height /2)))
        return scene