# Copyright 2026 James Adams
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import cadquery as cq
from cadqueryhelper import Base
from ..chip import ChipCan, Ring, RingConduit

from cqterrain.stairs.round import (
    greebled_stairs,
    ramp
)
from .RoundPlatform import RoundPlatform

class StairSegment(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.diameter:float = 73
        self.diameter_margin:float = 0.5
        self.height:float = 75 - 4
        
        self.render_can:bool = False
        self.render_stairs:bool = True
        self.render_ladder:bool = True
        self.stair_count:int = 11
        self.ramp_width:float = 64
        
        self.platform_height:float = 4
        self.platform_angle:float = 180
        
        self.ring_rotate:float = -45
        self.ring_padding:float = 10
        self.ring_height:float = 10
        
        #blueprints
        self.bp_can:Base|None = self.init_can()
        self.bp_ring:Base|None = self.init_ring()
        self.bp_platform:Base|None = RoundPlatform()
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.stairs:cq.Workplane|None = None
        self.platform:cq.Workplane|None = None
        
    def calculate_diameter(self):
        return self.diameter + self.diameter_margin
        
    def init_can(self):
        bp_can = ChipCan()
        bp_can.height = 194
        bp_can.diameter = self.diameter
        return bp_can
    
    def init_ring(self):
        bp_ring_conduit = RingConduit()
        bp_ring_conduit.inset = 5
        bp_ring_conduit.height = 10
        bp_ring_conduit.ladder_length = 25
        bp_ring_conduit.ladder_width = 10
        
        bp_ring_conduit.frame = 1
        bp_ring_conduit.frame_depth = 3
        bp_ring_conduit.pipe_count = None
        bp_ring_conduit.pipe_radius = 4
        bp_ring_conduit.pipe_inner_radius = 2
        bp_ring_conduit.segment_length = 6
        bp_ring_conduit.space = 4
        bp_ring_conduit.pipe_padding = 1
        return bp_ring_conduit
        
    def make_outline(self):
        outline = cq.Workplane("XY").cylinder(
            self.height,
            self.ramp_width
        )
        
        self.outline = outline
        
    def make_stairs(self):
        diameter = self.calculate_diameter()
        stairs = greebled_stairs(
            stair_count = self.stair_count,
            height = self.height,
            inner_diameter = diameter,
            diameter = diameter + self.ramp_width, 
            debug = False
        )
        
        round_ramp = ramp(
            stair_count = self.stair_count*2,
            height = self.height,
            inner_diameter = diameter,
            diameter = diameter + self.ramp_width,
            distance_overlap = 0.5,
            debug = False
        )
        
        round_ramp = (
            round_ramp
            .rotate((0,0,1),(0,0,0),-7)
        )
        
        stairs = (
            stairs
            .cut(round_ramp)
            .translate((0,0,(self.height)/2))
        )
        
        self.stairs = stairs
        
    def make_platform(self):
        diameter = self.calculate_diameter()
        self.bp_platform
        self.bp_platform.inner_diameter = diameter
        self.bp_platform.outer_diameter = diameter + self.ramp_width
        self.bp_platform.height = self.platform_height
        self.bp_platform.angle = self.platform_angle
        self.bp_platform.make()
   
        ex_platform = self.bp_platform.build()
        
        ex_platform = (
            ex_platform
            #.rotate((0,0,1),(0,0,0),self.platform_angle)
            #.translate((0,0,0))
        )
        self.platform = ex_platform

    def make(self):
        super().make()
        self.make_outline()
        
        if self.bp_can:
            self.bp_can.height = self.height
            self.bp_can.make()
            
        if self.bp_ring:
            diameter = self.calculate_diameter()
            self.bp_ring.render_ladders = self.render_ladder
            self.bp_ring.height = self.ring_height
            self.bp_ring.ladder_height = self.height
            self.bp_ring.cut_diameter = diameter
            self.bp_ring.diameter = self.bp_ring.cut_diameter + self.ring_padding
            self.bp_ring.make()

        if self.render_stairs:
            self.make_stairs()

        self.make_platform()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        #if self.outline:
        #    part = part.add(self.outline)
        
        if self.bp_can and self.render_can:
            can = self.bp_can.build()
            part = part.union(can.translate((0,0,self.bp_can.height/2)))
            
        if self.bp_ring:
            ring = self.bp_ring.build().rotate((0,0,1),(0,0,0),self.ring_rotate)
            part = part.union(ring)
            
        if self.stairs:
            part = part.union(self.stairs)
            
        if self.platform:
            ring = self.bp_ring.build().rotate((0,0,1),(0,0,0),self.ring_rotate)
            self.platform = self.platform.cut(ring)
            parts = part.add(self.platform)
        
        return part