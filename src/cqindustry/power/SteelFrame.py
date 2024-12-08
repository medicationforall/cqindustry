# Copyright 2023 James Adams
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
import math
from cadqueryhelper import Base, shape

class SteelFrame(Base):
    def __init__(self):
        super().__init__()
        self.length:float = 150
        self.width:float = 75
        self.height:float = 70
        
        self.segment_length:float = 75
        self.segment_width:float = 75
        
        self.z_width:float = 5
        self.z_height:float = 10
        self.z_web_thickness:float = 2
        self.z_flange_thickness:float = 2
        self.z_join_distance:float = 1.3
        
        self.y_width:float = 5
        self.y_height:float = 10
        self.y_web_thickness:float = 2
        self.y_flange_thickness:float = 2
        self.y_join_distance:float = 1.3
        
        self.render_debug_outline:bool = False
        self.render_debug_grid:bool = False
        
        #solids
        self.z_beam:cq.Workplane|None = None
        self.y_beam:cq.Workplane|None = None
        self.corner_joins:cq.Workplane|None = None
        self.z_grid:cq.Workplane|None = None
        self.y_grid:cq.Workplane|None = None
        self.corner_grid:cq.Workplane|None = None
        self.cube_grid:cq.Workplane|None = None
        
    def __make_z_beam(self):
        z_beam = shape.i_beam(
          length = self.height,
          width = self.z_width,
          height = self.z_height,
          web_thickness = self.z_web_thickness,
          flange_thickness = self.z_flange_thickness,
          join_distance = self.z_join_distance
        ).rotate((0,1,0),(0,0,0),90)
        self.z_beam = z_beam
        
    def __make_y_beam(self):
        y_count = math.floor(self.width / self.segment_width)
        
        y_beam = shape.i_beam(
          length = self.segment_width - (self.z_width/y_count),
          width = self.y_width,
          height = self.y_height,
          web_thickness = self.y_web_thickness,
          flange_thickness = self.z_flange_thickness,
          join_distance = self.y_join_distance
        ).rotate((0,0,1),(0,0,0),90)
        self.y_beam = y_beam
        
    def __make_corner_joins(self):
        y_count = math.floor(self.width / self.segment_width)
        x_translate = self.segment_width/2 - (self.z_width/(y_count)) - 1*y_count#- 5 - 5/2 +1.5
        z_translate = self.height/2 - self.y_height/2 - 5/2
        corner_join = (
            shape.corner_join(5,5,self.y_width,1,1)
            .rotate((0,1,0),(0,0,0),90)
        )
        
        frame_joins = (
            cq.Workplane("XY")
            .union(corner_join.translate((0,x_translate,z_translate)))
            .union(corner_join.rotate((0,0,1),(0,0,0),180).translate((0,-x_translate,z_translate)))
        )

        self.corner_joins = frame_joins
        
    def __make_z_grid(self):
        def add_z_beam(loc:cq.Location)->cq.Shape:
            return self.z_beam.val().located(loc)#type:ignore
        
        x_count = math.floor(self.length / self.segment_length)
        y_count = math.floor(self.width / self.segment_width)

        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.segment_length - (self.z_height/x_count), 
                ySpacing = self.segment_width - (self.z_width/y_count),
                xCount = x_count+1, 
                yCount= y_count+1, 
                center = True)
            .eachpoint(callback = add_z_beam)
        )
        self.z_grid = result
        
    def __make_y_grid(self):
        def add_y_beam(loc:cq.Location)->cq.Shape:
            return self.y_beam.val().located(loc)#type:ignore
        
        x_count = math.floor(self.length / self.segment_length)
        y_count = math.floor(self.width / self.segment_width)

        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.segment_length - (self.z_height/(x_count)), 
                ySpacing = self.segment_width - (self.z_width/(y_count)),
                xCount = x_count+1, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_y_beam)
        ).translate((0,0,self.height/2))
        self.y_grid = result
        
    def __make_corner_grid(self):
        def add_y_corners(loc:cq.Location)->cq.Shape:
            return self.corner_joins.val().located(loc)#type:ignore
        
        x_count = math.floor(self.length / self.segment_length)
        y_count = math.floor(self.width / self.segment_width)
        
        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.segment_length - (self.z_height/(x_count)), 
                ySpacing = self.segment_width - (self.z_width/(y_count)),
                xCount = x_count+1, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_y_corners)
        )
        self.corner_grid = result
        
        
    def __make_cube_grid(self):
        x_count = math.floor(self.length / self.segment_length)
        y_count = math.floor(self.width / self.segment_width)

        def add_cube(loc:cq.Location)->cq.Shape:
            return cq.Workplane("XY").box(
                self.segment_length - (self.z_height/x_count), 
                self.segment_width - (self.z_width/y_count), 
                self.height).val().located(loc)#type:ignore
        
        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = self.segment_length - (self.z_height/x_count), 
                ySpacing = self.segment_width - (self.z_width/y_count),
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_cube)
        )
        self.cube_grid = result
        
    def make(self, parent="none"):
        super().make(parent)
        self.__make_z_beam()
        self.__make_y_beam()
        self.__make_corner_joins()
        self.__make_z_grid()
        self.__make_y_grid()
        self.__make_corner_grid()
        self.__make_cube_grid()
        
    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
        )
        
        if self.render_debug_grid and self.cube_grid:
            scene = scene.add(self.cube_grid)
        
        if self.z_grid and self.y_grid and self.corner_grid:
            scene = (
                scene
                .add(self.z_grid)
                .add(self.y_grid)
                .add(self.corner_grid)
            )
        
        if self.render_debug_outline:
            outline = cq.Workplane("XY").box(self.length, self.width, self.height)
            scene = scene.add(outline)
            
        return scene