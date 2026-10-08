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
from . import Wall
from cadqueryhelper import Base
from cqterrain.ruin import ruin_segment_random
from typing import Literal

class WallRuinSegment(Wall):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 75
        self.width:float = 30
        self.height:float = 25
        self.ruin_seed:str|None = None
        self.panel_cut_seed:str|None = None
        self.ruin_shift: tuple[float, float, float] = (-1,3,1)
        self.vertical_beam_count:int = 2
        
        self.debug:bool = False
        self.direction:Literal['top','bottom']= 'top'
        self.ruin_height:float = 12.5
        self.ruin_points:float = 7
        self.ruin_padding:float = -10
        
        #shapes
        self.ruin_corner:cq.Workplane|None = None
        self.panel_cut:cq.Workplane|None = None
        self.outline:cq.Workplane|None = None
        
    def make_ruin(self):
        seed = self.seed+"_corner"
        
        if self.ruin_seed:
            seed = self.ruin_seed
        
        ruin_corner = ruin_segment_random(
            length = self.length + self.ruin_padding, 
            width = self.ruin_height, 
            height = self.beam_height, 
            points = (self.ruin_points, self.ruin_points, self.ruin_points),
            debug = False,
            shift = self.ruin_shift,
            seed = seed
        )
        
        
        if self.direction == 'bottom':
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .translate((0,-self.beam_height/2,0))
            )
        else:
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .rotate((0,0,1),(0,0,0),180)
                .rotate((0,1,0),(0,0,0),180)
                .translate((0,-self.beam_height+(-self.beam_height/2),self.beam_length))
            )
        
        self.ruin_corner = ruin_corner
        
    def make_panel_cut(self):
        seed = self.seed+"_panel"
        
        if self.panel_cut_seed:
            seed = self.panel_cut_seed
            
        length = self.length + 5
        height = self.ruin_height + 3
        
        ruin_corner = ruin_segment_random(
            length = self.length + self.ruin_padding, 
            width = height, 
            height = self.beam_height, 
            points = (self.ruin_points, self.ruin_points, self.ruin_points),
            debug = False,
            shift = self.ruin_shift,
            seed = seed
        )
        
        
        if self.direction == 'bottom':
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .translate((0,-self.beam_height/2,0))
            )
        else:
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .rotate((0,0,1),(0,0,0),180)
                .rotate((0,1,0),(0,0,0),180)
                .translate((0,-self.beam_height+(-self.beam_height/2),self.beam_length+5))
            )

        self.panel_cut = ruin_corner
        
    def make(self):
        super().make()
        self.make_ruin()
        self.make_panel_cut()

        
    def build(self)->cq.Workplane:
        if self.make_called == False:
            raise Exception('Make has not been called')
        
        part = cq.Workplane("XY")

        if self.base:
            part = part.add(self.base)
            
            
        beams = cq.Workplane("XY")
        if self.vertical_beams:
            beams = beams.union(self.vertical_beams)
            
        if self.h_beams:
            beams = beams.add(self.h_beams)
            
        if beams:
            part = part.add(beams)
            
        if self.grid:
            
            if self.debug:
                l_grid = (
                    self.grid
                    .add(self.ruin_corner)
                )
            else:
                if self.direction == 'bottom':
                    l_grid = (
                        self.grid
                        .intersect(self.ruin_corner)
                    )
                else:
                    l_grid = (
                        self.grid
                        .cut(self.ruin_corner)
                    )
            part = part.add(l_grid)
        
        if self.s_panels:
            
            if self.debug:
                l_panels = (
                    self.s_panels
                    .add(self.panel_cut.translate((0,-2,0)))
                )
            else:
                if self.direction == 'bottom':
                    l_panels = (
                        self.s_panels
                        .intersect(self.panel_cut.translate((0,-2,0)))
                    )
                else:
                    l_panels = (
                        self.s_panels
                        .cut(self.panel_cut.translate((0,-2,0)))
                    )
            
            part = part.add(l_panels)
        
        return part
    
    def build_assembly(self)->cq.Assembly:
        if self.make_called == False:
            raise Exception('Make has not been called')

        assembly = cq.Assembly()
        part = cq.Workplane()

        if self.base:
            a_base = self.base#translate((0,0,-self.base_height/2))
            assembly.add(a_base, color=cq.Color(0, 0, 1), name="base")
            
            
        beams = cq.Workplane("XY")
        if self.vertical_beams:
            beams = beams.union(self.vertical_beams)
            
        if self.h_beams:
            beams = beams.add(self.h_beams)
            
        if beams:
                assembly.add(beams, color=cq.Color(0, 1, 0), name="beams")
            
        if self.grid:
            if self.direction == 'bottom':
                l_grid = (
                    self.grid
                    .intersect(self.ruin_corner)
                )
            else:
                l_grid = (
                    self.grid
                    .cut(self.ruin_corner)
                )

            assembly.add(l_grid, color=cq.Color(1, 0, 0), name="grid")
        
        if self.s_panels:
            if self.direction == 'bottom':
                l_panels = (
                    self.s_panels
                    .intersect(self.panel_cut.translate((0,-2,0)))
                )
            else:
                l_panels = (
                    self.s_panels
                    .cut(self.panel_cut.translate((0,-2,0)))
                )
            
            assembly.add(l_panels, color=cq.Color(1, 1, 0), name="panels")

        return assembly