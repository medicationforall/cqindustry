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
from cqindustry.chip import ChipCan
from cqindustry.can import StairSegment
from cqterrain.greeble import cap_greeble
from cqterrain import pipe
from cqindustry.can import RoundPlatformGreebledCircles

class CanTowerStairs(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.diameter:float = 73
        #self.length:float = 30
        #self.width:float = 25
        self.height:float = 194
        
        self.render_can:bool = True
        self.render_pipe:bool = True
        
        #blueprints
        self.bp_can:base|None = self.init_can()
        self.bp_floor_one:base|None = self.init_floor_one()
        self.bp_floor_two:base|None = self.init_floor_two()
        self.bp_floor_three:base|None = self.init_floor_three()
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.pipe = None
        self.cut_pipe = None
        self.cap = None
        
    def init_can(self)->Base:
        bp_can = ChipCan()
        bp_can.height = 194
        bp_can.diameter = self.diameter
        return bp_can
    
    def init_floor_one(self)->Base:
        bp_floor = StairSegment()
        bp_floor.ring_height = 23.5
        bp_floor.platform_angle = 29
        
        bp_platform = RoundPlatformGreebledCircles()
        bp_platform.rows = 4
        bp_platform.taper = None
        bp_platform.circle_diameter = 2.5
        bp_platform.spacing = 7
        bp_floor.bp_platform = bp_platform
        return bp_floor
    
    def init_floor_two(self)->Base:
        bp_floor = StairSegment()
        bp_floor.height = 75
        
        bp_platform = RoundPlatformGreebledCircles()
        bp_platform.rows = 12
        bp_platform.taper = None
        bp_platform.circle_diameter = 2.5
        bp_platform.spacing = 7
        bp_floor.bp_platform = bp_platform
        
        return bp_floor
    
    def init_floor_three(self)->Base:
        bp_floor = StairSegment()
        bp_floor.platform_angle = 90
        bp_floor.render_ladder = False
        bp_floor.render_stairs = False
        
        bp_platform = RoundPlatformGreebledCircles()
        bp_platform.rows = 6
        bp_platform.taper = None
        bp_platform.circle_diameter = 2.5
        bp_platform.spacing = 7
        bp_floor.bp_platform = bp_platform
        
        return bp_floor
        
    #def make_outline(self):
    #    outline = cq.Workplane("XY").box(
    #        self.length,
    #        self.width,
    #        self.height
    #    )
        
    #    self.outline = outline
        
    def make_cap(self):
        self.cap = cap_greeble(
            diameter = 60, 
            teeth = 14,
            rotate_teeth = 30,
            body_height = 3,
            teeth_diameter = 3,
            chamfer = 2,
            interior_height = 2,
            interior_diameter = 6,
            interior_cut_diameter = 8,
            bars_count = 12,
            bar_length = 23,
            bar_diameter = 2
        )
        
    def make_pipe(self):
        pipe_line = pipe.straight(
            length = 73+10+2, 
            connector_length=2, 
            connector_radius = 11.5,
            render_hollow=False,
            render_through_hole=False
        )
        
        self.pipe = pipe_line
        
    def make_cut_pipe(self):
        diameter = self.bp_floor_one.calculate_diameter()
        cut_pipe = cq.Workplane("XY").cylinder(23.5, diameter/2)
        self.cut_pipe = cut_pipe.translate((0,0,23.5/2))
        
    def make(self):
        super().make()
        #self.make_outline()
        
        if self.bp_can:
            self.bp_can.height = self.height
            self.bp_can.diameter = self.diameter
            self.bp_can.make()
            
        if self.bp_floor_one:
            self.bp_floor_one.diameter = self.diameter
            self.bp_floor_one.make()
            if self.render_pipe:
                self.make_pipe()
                self.make_cut_pipe()
            
        if self.bp_floor_two:
            self.bp_floor_two.diameter = self.diameter
            self.bp_floor_two.make()
            
        if self.bp_floor_three:
            self.bp_floor_three.diameter = self.diameter
            self.bp_floor_three.make()
            
        self.make_cap()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        #if self.outline:
        #    part = part.add(self.outline)
        
        if self.bp_can and self.render_can:
            can = self.bp_can.build()
            part = part.union(can.translate((0,0,self.bp_can.height/2)))
        
        return part
    
    def build_can(self)->cq.Workplane:
        part = cq.Workplane("XY")
        can = self.bp_can.build()
        part = part.union(can.translate((0,0,self.bp_can.height/2)))
        return part
        
    
    def build_floor_one(self)->cq.Workplane:
        part = cq.Workplane("XY")
        if self.bp_floor_one:
            floor_one = self.bp_floor_one.build()
            part = part.add(floor_one)
            
            if self.render_pipe and self.pipe:
                pipe = self.pipe.cut(self.cut_pipe)
                part = part.union(pipe.rotate((0,0,1),(0,0,0),90))
                
        return part
    
    def build_floor_two(self)->cq.Workplane:
        part = cq.Workplane("XY")
        if self.bp_floor_two:
            translate_z = self.bp_floor_one.height
            rotate_degrees = 90
            floor_two = (
                self.bp_floor_two
                .build()
                .rotate((0,0,1),(0,0,0),rotate_degrees)
                .translate((0,0,translate_z))
            )
            part = part.add(floor_two)
                
        return part
    
    def build_floor_three(self)->cq.Workplane:
        part = cq.Workplane("XY")
        if self.bp_floor_three:
            translate_z = self.bp_floor_one.height + self.bp_floor_two.height
            rotate_degrees = 90
            floor_three = (
                self.bp_floor_three
                .build()
                .rotate((0,0,1),(0,0,0),-rotate_degrees)
                .translate((0,0,translate_z))
            )
            part = part.add(floor_three)
                
        return part
    
    def build_cap(self)->cq.Workplane:
        part = cq.Workplane("XY")
        if self.cap:
            part = part.add(self.cap.translate((0,0,self.height)))
                
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        #if self.outline:
        #    part = part.add(self.outline)
        
        if self.bp_can and self.render_can:
            can = self.bp_can.build()
            part = part.union(can.translate((0,0,self.bp_can.height/2)))
            
        if self.bp_floor_one:
            floor_one = self.bp_floor_one.build()
            part = part.add(floor_one)
            
            if self.render_pipe and self.pipe:
                pipe = self.pipe.cut(self.cut_pipe)
                part = part.union(pipe.rotate((0,0,1),(0,0,0),90))
            
        if self.bp_floor_two:
            translate_z = self.bp_floor_one.height
            rotate_degrees = 90
            floor_two = (
                self.bp_floor_two
                .build()
                .rotate((0,0,1),(0,0,0),rotate_degrees)
                .translate((0,0,translate_z))
            )
            part = part.add(floor_two)
            
        if self.bp_floor_three:
            translate_z = self.bp_floor_one.height + self.bp_floor_two.height
            rotate_degrees = 90
            floor_three = (
                self.bp_floor_three
                .build()
                .rotate((0,0,1),(0,0,0),-rotate_degrees)
                .translate((0,0,translate_z))
            )
            part = part.add(floor_three)
            
        if self.cap:
            part = part.add(self.cap.translate((0,0,self.height)))
        
        return part