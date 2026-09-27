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
from cqterrain.minibase import slot, ellipse, slot_uneven, circle_uneven
from cadqueryhelper.shape import i_beam

from cadqueryhelper.grid import (
    grid_points,
    cell_stretch_points_random,
    grid_cell_random
    #grid_cell_basic,
    #grid_cell_random
)
import random
from typing import Callable
from cqterrain import tile, greeble
from math import floor
from . import stylized_panels

from .tiles import (
    plain,
    slot,
    rivet,
    vent,
    bolt_panel,
    corrugated,
    charge
)


class Wall(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 75
        self.width:float = 25
        self.height:float = 60

        self.seed:str = 'debris'
        self.base_height:float = 3
        self.vertical_beam_count:int = 2
        self.verical_beam_width:float = 5
        
        self.beam_length:float = 25
        self.beam_height:float = 10
        self.web_thickness:float = 2
        self.length_inset:float = 15

        self.tiles:list[Callable[[float,float,float],cq.Workplane]] = [
            #plain,
            bolt_panel,
            bolt_panel,
            charge,
            rivet,
            rivet,
            slot,
            slot,
            vent, 
            corrugated,
            corrugated
        ]

        self.render_grid:bool = True
        self.grid_x_spacing:float = 5
        self.grid_y_spacing:float = 5
        self.grid_x_stretch:tuple[int,int,int]|int = (1,4,1)
        self.grid_y_stretch:tuple[int,int,int]|int = (1,3,1)
        self.grid_height:float|tuple[float,float,float]=(2,3,1)

        self.h_bleam_width:float = 5
        self.h_beam_height:float = 10

        self.render_panels:bool = True
        self.panel_seed:str|None = None
        self.panel_width:float = 10
        self.panel_count:int|tuple[int,int,int] = (2,3,1)
        self.panel_rotate:float|tuple[float,float,float] = (-45,45,5)
        self.panel_tiles:list[Callable[[float,float,float],cq.Workplane]] = [rivet,bolt_panel]

        #shapes
        self.outline:cq.Workplane|None = None
        self.base:cq.Workplane|None = None
        self.vertical_beams:cq.Workplane|None = None
        self.h_beams:cq.Workplane|None = None
        self.grid:cq.Workplane|None = None
        self.s_panels:cq.Workplane|None = None
        
    def calculate_x_space(self)->float:
        vert_length = self.length - self.length_inset
        x_count = self.vertical_beam_count

        if x_count == 1:
            x_space = vert_length
        else:
            x_space = vert_length/(x_count-1)
        return x_space
    
    def make_outline(self)->cq.Workplane:
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline

    def make_base(self):

        if self.length == self.width:
            base = circle_uneven(
                diameter = self.length,
                base_height = self.base_height,
                taper = -1,
                render_magnet = True,  
                magnet_diameter = 3, 
                magnet_height = 2,
                detail_height = 2,
                uneven_height = 3,
                peak_count = (9,10),
                segments = 6,
                seed = self.seed
            ).translate((0,0,-self.base_height/2))
        else:
            base = slot_uneven(
                length = self.length,
                width = self.width,
                base_height = self.base_height,
                taper = -1,
                render_magnet = True,  
                magnet_diameter = 3, 
                magnet_height = 2,
                detail_height = 2,
                uneven_height = 3,
                peak_count = (9,10),
                segments = 6,
                seed = self.seed
            ).translate((0,0,-self.base_height/2))
        self.base = base
        
    def make_vertical_beams(self):
        beam = i_beam(
          length=self.beam_length,
          width=self.verical_beam_width,
          height=self.beam_height,
          web_thickness=self.web_thickness,
          flange_thickness=2,
          join_distance=1.3
        )
        
        vertical_beam = (
            beam
            .rotate((0,1,0),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),90)
            .translate((0,0,self.beam_length/2))
        )
        
        vert_length = self.length - self.length_inset
        vertical_beams = cq.Workplane("XY")
        x_count = self.vertical_beam_count
        x_space = self.calculate_x_space()

        for i in range(x_count):
            vertical_beams = vertical_beams.add(vertical_beam.translate((i*x_space,0,0)))
        
        if x_count  >   1:
            self.vertical_beams = vertical_beams.translate((-vert_length/2,0,0))
        else:
            self.vertical_beams = vertical_beams
        
    def make_horizontal_beams(self):
        x_count = self.vertical_beam_count
        x_space = self.calculate_x_space()
        h_beam_length = x_space - self.web_thickness
        
        horizontal_beam = i_beam(
          length=h_beam_length,
          width = self.h_bleam_width,
          height = self.h_beam_height,
          web_thickness=2,
          flange_thickness=2,
          join_distance=1.3
        ).translate((0,0,self.beam_length/2))
        
        
        h_count = x_count -1
        h_space = h_beam_length + self.web_thickness
        h_beams = cq.Workplane("XY")
        
        for i in range(h_count):
            h_beams = h_beams.add(horizontal_beam.translate((i*h_space,0,0)))
        
        if x_count >2:
            h_beams = h_beams.translate((floor(h_space/2) - ((h_count/2)*h_space),0,0))
                
        self.h_beams = h_beams
        
    def make_grid(self):
        
        columns = floor(self.length/self.grid_x_spacing)+1
        rows = floor(self.beam_length/self.grid_y_spacing)+1
        
        points, stream = grid_points(
            columns = columns,
            rows = rows,
            x_spacing = self.grid_x_spacing,
            y_spacing = self.grid_y_spacing
        )
        
        cell_points = cell_stretch_points_random(
            points,
            x_stretch = self.grid_x_stretch,
            y_stretch = self.grid_y_stretch,
            seed=self.seed,
            uniform_split = True
        )
        
        grid = grid_cell_random(
            cell_points,
            height = self.grid_height,
            offset = 0,
            taper = (5,25,5),
            seed=self.seed,
            tiles = self.tiles
        )
        
        z_translate = self.beam_length
        
        grid = (
            grid
            .translate((-self.length/2,0,0))
            .rotate((1,0,0),(0,0,0),-90)
            .translate((0,-self.beam_height/2,z_translate))
        )
        
        self.grid = grid
        
    def make_panels(self):
        z_translate = self.beam_length
        seed = self.seed

        if self.panel_seed:
            seed = self.panel_seed
        
        s_panels = (
            stylized_panels(
                length = self.length,
                width = self.panel_width,
                height = 2,
                count= self.panel_count,
                seed=seed,
                rotate = self.panel_rotate,
                tiles = self.panel_tiles
            )
            .rotate((1,0,0),(0,0,0),-90)
            .translate((0,-self.beam_height/2-3,z_translate/2))
        )
        
        self.s_panels = s_panels


    def make(self):
        super().make()
        self.make_outline()
        self.make_base()
        self.make_vertical_beams()
        self.make_horizontal_beams()
        if self.render_grid:
            self.make_grid()

        if self.render_panels:
            self.make_panels()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.base:
            part = part.add(self.base)
            
        if self.vertical_beams:
            part = part.union(self.vertical_beams)
            
        if self.h_beams:
            part = part.add(self.h_beams)
            
        if self.grid:
            part = part.add(self.grid)
        
        if self.s_panels:
            part = part.add(self.s_panels)
        
        return part.translate((0,0,self.base_height))


    def build_assembly(self) -> cq.Assembly:
        super().build()
        assembly = cq.Assembly()

        if self.base:
            a_base = self.base#translate((0,0,-self.base_height/2))
            assembly.add(a_base, color=cq.Color(0, 0, 1), name="base")
            
        if self.vertical_beams:
            a_beams = cq.Workplane("XY")

            if self.vertical_beams:
                a_beams = a_beams.union(self.vertical_beams)

            if self.h_beams:
                a_beams = a_beams.add(self.h_beams)

            assembly.add(a_beams, color=cq.Color(0, 1, 0), name="beams")
            
        if self.grid:
            assembly.add(self.grid, color=cq.Color(1, 0, 0), name="grid")
        
        if self.s_panels:
            assembly.add(self.s_panels, color=cq.Color(1, 1, 0), name="panels")
        
        return assembly

