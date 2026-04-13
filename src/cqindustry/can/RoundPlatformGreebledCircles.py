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
import math
from cadqueryhelper.shape import (
    cylinder_sector
)
from cadqueryhelper import Base
from cadqueryhelper.grid import (
    grid_arc_points, 
    cell_stretch_points, 
    grid_cell_basic
)
from .RoundPlatform import RoundPlatform

class RoundPlatformGreebledCircles(RoundPlatform):
    def __init__(self):
        super().__init__()
        #parameters
        self.tile_height:float = 2
        self.frame_width:float = 2
        self.spacing:float = 5
        self.taper:float|None = None
        self.rows:int = 13
        self.offset:float = -1
        self.circle_diameter:float = 2
        self.cut_circle_diameter:float = 1.5
        self.circle_max_index:float = 1

        #shapes
        self.platform = None
        self.frame_cut = None
        self.frame = None
        self.points = None
        self.lines = None
        self.circles = None
        self.cut_circles = None
        
    def make_platform(self):
        diameter = self.inner_diameter
        cut_platform  = cylinder_sector(
            diameter = diameter,
            angle = self.angle,
            height = self.height
        )
        
        ex_platform = cylinder_sector(
            diameter = self.outer_diameter,  
            angle = self.angle,
            height = self.height
        )
        
        ex_platform = ex_platform.cut(cut_platform)
        
        ex_platform = (
            ex_platform
            .rotate((0,0,1),(0,0,0),self.angle)
            .translate((0,0,0))
        )
        self.platform = ex_platform
        
    def make_frame_cut(self):
        face = self.platform.faces(">Z").edges().toPending().offset2D(-self.frame_width).extrude(-self.tile_height, combine="cut")
        self.frame = face
        self.frame_cut = self.platform.cut(self.frame)
        
    def make_grid(self):
        outer_columns = math.ceil((self.outer_diameter/2) / self.spacing)
        inner_columns = math.ceil((self.inner_diameter/2) / self.spacing)
        #log(inner_columns)
        points, stream = grid_arc_points(
            columns = outer_columns,
            rows = self.rows,
            x_spacing = self.spacing,
            angle = self.angle
        )
        
        points_cutoff = (inner_columns-1) * self.rows
        
        cell_points = cell_stretch_points(
            points[inner_columns-1:],
            x_stretch = 1,
            y_stretch = 1
        )
        
        grid = grid_cell_basic(
            cell_points,
            height = self.tile_height,
            taper = self.taper,
            offset = self.offset
        ).translate((0,0,self.height-self.tile_height))
        
        grid_intersect = self.frame_cut.intersect(grid)
        
        #example = cq.Workplane("XY").pushPoints(stream[points_cutoff:]).box(1,1,1)
        
        self.points = grid_intersect
        
    def make_circles(self):
        circle = (
            cq.Workplane("XY")
            .cylinder(self.tile_height, self.circle_diameter)
            .translate((0,0,self.height/2+self.tile_height/2))
        )
        
        outer_columns = math.ceil((self.outer_diameter/2) / self.spacing)
        inner_columns = math.ceil((self.inner_diameter/2) / self.spacing)
        
        points, stream = grid_arc_points(
            columns = outer_columns,
            rows = self.rows,
            x_spacing = self.spacing,
            angle = self.angle
        )
        
        def add_circle(loc):
            return circle.val().located(loc)
        
        new_points = points
        
        new_stream = []
        for point_list in new_points[inner_columns:-self.circle_max_index]:
            new_stream += point_list[1:-1]
        
        self.circles = (
            cq.Workplane("XY")
            .pushPoints(new_stream)
            .eachpoint(add_circle)
        )
        
    def make_cut_circles(self):
        circle = (
            cq.Workplane("XY")
            .cylinder(self.tile_height, self.cut_circle_diameter)
            .translate((0, 0, self.height/2+self.tile_height/2))
        )
        
        outer_columns = math.ceil((self.outer_diameter/2) / self.spacing)
        inner_columns = math.ceil((self.inner_diameter/2) / self.spacing)
        
        points, stream = grid_arc_points(
            columns = outer_columns,
            rows = self.rows,
            x_spacing = self.spacing,
            angle = self.angle
        )
        
        def add_circle(loc):
            return circle.val().located(loc)
        
        new_points = points
        
        new_stream = []
        for point_list in new_points[inner_columns:-self.circle_max_index]:
            new_stream += point_list[1:-1]
        
        self.cut_circles = (
            cq.Workplane("XY")
            .pushPoints(new_stream)
            .eachpoint(add_circle)
        )
        
    def make_lines(self):
        self.lines = self.frame_cut.cut(self.points)
        
        
    def make(self):
        #self.make_called = True
        super().make()
        self.make_frame_cut()
        self.make_grid()
        self.make_lines()
        self.make_circles()
        self.make_cut_circles()
        
    def build(self)->cq.Workplane:
        part = super().build()
        
        if self.frame_cut:
            part = self.frame
            
        if self.points:
            part = part.union(self.lines)
            #return self.points
            
        if self.circles:
            part = part.union(self.circles)
            
        if self.cut_circles:
            part = part.cut(self.cut_circles)
        
        return part