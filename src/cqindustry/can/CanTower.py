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

        self.render_rails:bool = True
        self.render_pipe:bool = True
        self.render_platform:bool = True
        self.render_ring:bool = True
        
        #blueprints
        self.bp_ring:Ring = Ring()
        self.bp_ring.height = 10
        self.bp_ring.ladder_width = 5
        
        self.bp_can:ChipCan = ChipCan()
        self.bp_chip_cut:ChipCan = ChipCan()
        
        self.bp_platform:CanPlatform = CanPlatform()
        self.bp_rail:CanRail|None = CanRail()
        
        #shapes
        self.pipe:cq.Workplane|None = None

    def make_ring(self):
        if self.render_ring:
            self.bp_ring.diameter = self.can_diameter + (self.ring_width*2)
            self.bp_ring.cut_diameter = self.can_diameter + self.cut_padding
            self.bp_ring.ladder_height = self.can_height - self.platform_height/2
            self.bp_ring.make()

    def make_can(self):
        self.bp_can.height = self.can_height
        self.bp_can.diameter = self.can_diameter
        self.bp_can.make()

    def make_chip_cut(self):
        self.bp_chip_cut.height = self.can_height
        self.bp_chip_cut.diameter = self.can_diameter + self.cut_padding
        self.bp_chip_cut.make()

    def make_platform(self):
        if self.render_platform or self.render_rails:
            self.bp_platform.diameter = self.can_diameter + (self.ring_width*2)
            self.bp_platform.cut_diameter = self.can_diameter + self.cut_padding
            self.bp_platform.height = self.platform_height
            self.bp_platform.cut_height = self.platform_height/2
            self.bp_platform.ladder_height = self.platform_height + self.platform_ladder_extends
            self.bp_platform.make()
        
    def make(self, parent=None):
        super().make(parent)
        
        self.make_ring()
        self.make_can()
        self.make_chip_cut()
        self.make_platform()
        
        if self.render_rails and self.bp_rail:
            self.bp_rail.make(self.bp_platform)
        
        if self.render_pipe:
            self.pipe = straight(length = self.pipe_length, render_hollow=False, render_through_hole = False)

    def build_ring_pipe_connector(self):
        ring = self.bp_ring.build()
        
        scene = cq.Workplane("XY")
        scene = (
            scene
            .union(ring)
        )

        if self.render_pipe and self.pipe:
            pipe = self.pipe
            soda_can_cut = self.bp_chip_cut.build()
            #print('build_ring_pipe_connector - add pipe')

            pipe = pipe.cut(soda_can_cut.translate((0,0,self.bp_can.height /2)))
            scene = (
                scene.union(pipe)
            )
        else:
            print('Skipped pipe')

        #print('build_ring_pipe_connector - return results')
        return scene

    def build(self):
        scene = (
            cq.Workplane("XY")
        )

        if self.render_platform and self.bp_platform:
            #print('CanTower build platform')
            platform = self.bp_platform.build()
            scene = scene.union(platform.translate((0,0,self.bp_can.height))) 

        if self.render_rails and self.bp_rail:
            #print('CanTower build rail')
            rail = self.bp_rail.build()
            scene = scene.union(rail.translate((0,0,self.bp_can.height)))

        if self.render_can and self.bp_can:
            #print('CanTower build can')
            soda_can = self.bp_can.build()
            scene = scene.union(soda_can.translate((0,0,self.bp_can.height /2)))

        if self.render_ring:
            #print('CanTower build ring')
            ring = self.build_ring_pipe_connector()
            scene = scene.union(ring)

        #print('CanTower finished build return result')
        return scene
    
    def build_plate(self):
        scene = (cq.Workplane("XY"))

        if self.render_ring:
            ring = self.build_ring_pipe_connector()
            scene = scene.union(ring)

        if self.render_platform and self.bp_platform:
            platform = self.bp_platform.build()
            scene = scene.add(platform.translate((0,self.can_diameter+self.ring_width+10,self.bp_platform.height/2))) 

        if self.render_rails and self.bp_rail:
            rail = self.bp_rail.build()
            scene = scene.add(rail.rotate((0,1,0),(0,0,0),180).translate((0,(self.can_diameter+self.ring_width+10)*2,self.bp_rail.height+(self.bp_platform.height/2))))

        return scene