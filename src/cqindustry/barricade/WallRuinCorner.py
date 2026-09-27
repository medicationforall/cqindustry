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
from cqterrain.ruin import ruin_corner_random

class WallRuinCorner(Wall):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 30
        self.width:float = 30
        self.height:float = 25
        self.ruin_seed:str|None = None
        self.beam_cut_seed:str|None = None
        self.panel_cut_seed:str|None = None
        self.ruin_shift = (-3,3,1)
        self.vertical_beam_count = 1
        
        self.debug:bool = False
        self.direction:Literal['left','right']= 'right'
        
        #shapes
        self.ruin_corner = None
        self.beam_cut = None
        self.panel_cut = None
        self.outline:cq.Workplane|None = None
        
    def make_ruin_corner(self):
        seed = self.seed+"_corner"
        
        if self.ruin_seed:
            seed = self.ruin_seed
        
        ruin_corner = ruin_corner_random(
            length = self.length, 
            width = self.height, 
            height = self.beam_height, 
            points = 7,
            debug = False,
            shift = self.ruin_shift,
            seed = seed
        )
        
        if self.direction == 'right':
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .translate((-self.length/2,-self.beam_height/2,0))
            )
        else:
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .rotate((0,0,1),(0,0,0),180)
                .translate((self.length/2,-self.beam_height+(-self.beam_height/2),0))
            )
        
        self.ruin_corner = ruin_corner
        
    def make_beam_cut(self):
        seed = self.seed+"_beam"
        
        if self.beam_cut_seed:
            seed = self.beam_cut_seed
            
        length = self.length + 5
        height = self.height + 5
        
        ruin_corner = ruin_corner_random(
            length = length, 
            width = height, 
            height = self.beam_height, 
            points = 7,
            debug = False,
            shift = self.ruin_shift,
            seed = seed
        )
        
        if self.direction == 'right':
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .translate((-self.length/2,-self.beam_height/2,0))
            )
        else:
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .rotate((0,0,1),(0,0,0),180)
                .translate((self.length/2,-self.beam_height+(-self.beam_height/2),0))
            )
        
        self.beam_cut = ruin_corner
        
    def make_panel_cut(self):
        seed = self.seed+"_panel"
        
        if self.panel_cut_seed:
            seed = self.panel_cut_seed
            
        length = self.length + 5
        height = self.height + 1
        
        ruin_corner = ruin_corner_random(
            length = length, 
            width = height, 
            height = self.beam_height, 
            points = 7,
            debug = False,
            shift = self.ruin_shift,
            seed = seed
        )
        
        
        if self.direction == 'right':
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .translate((-length/2,-self.beam_height/2,0))
            )
        else:
            ruin_corner = (
                ruin_corner
                .rotate((1,0,0),(0,0,0),-90)
                .rotate((0,0,1),(0,0,0),180)
                .translate((length/2,-self.beam_height+(-self.beam_height/2),0))
            )

        self.panel_cut = ruin_corner
        
    def make(self):
        super().make()
        self.make_ruin_corner()
        self.make_beam_cut()
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
            if self.debug:
                beams = (
                    beams
                    .add(self.beam_cut.translate((0,self.beam_height,0)))
                )
            else:
                beams = beams.intersect(self.beam_cut.translate((0,self.beam_height,0)))
            
            part = part.add(beams)
            
        if self.grid:
            
            if self.debug:
                l_grid = (
                    self.grid
                    #.add(self.ruin_corner)
                )
            else:
                l_grid = (
                    self.grid
                    .intersect(self.ruin_corner)
                )
            part = part.add(l_grid)
        
        if self.s_panels:
            
            if self.debug:
                l_panels = (
                    self.s_panels
                    .add(self.panel_cut.translate((0,-2,0)))
                )
            else:
                l_panels = (
                    self.s_panels
                    .intersect(self.panel_cut.translate((0,-2,0)))
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
                beams = beams.intersect(self.beam_cut.translate((0,self.beam_height,0)))
                assembly.add(beams, color=cq.Color(0, 1, 0), name="beams")
            
        if self.grid:
            l_grid = (
                self.grid
                .intersect(self.ruin_corner)
            )
            assembly.add(l_grid, color=cq.Color(1, 0, 0), name="grid")
        
        if self.s_panels:
            l_panels = (
                self.s_panels
                .intersect(self.panel_cut.translate((0,-2,0)))
            )
            
            assembly.add(l_panels, color=cq.Color(1, 1, 0), name="panels")

        return assembly