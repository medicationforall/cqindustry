# Copyright 2024 James Adams
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
from cadqueryhelper import shape
from cadqueryhelper.grid import irregular_grid
from . import Frame
from cqterrain.shieldwall import CapGreeble

class FrameBlock(Frame):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.seed:str|None = 'test'
        self.max_columns:int = 2
        self.max_rows:int = 3
        self.col_size:float = 10
        self.row_size:float = 10
        self.passes_count:int = 1000
        self.power_offset:float  = 4
        
        # blueprints
        self.bp_power:CapGreeble|None = CapGreeble()
        self.bp_power.width = 19
        self.bp_power.height = 30
        self.bp_power.top_fillet = 2.9
        self.bp_power.side_fillet = 3
        self.bp_power.operation = 'chamfer'
        self.bp_power.render_grill = True
        self.bp_power.grill_height = 2
        self.bp_power.grill_padding_top = 1
        self.bp_power.grill_padding_left = 2
        self.bp_power.grill_margin = .75
        
        # shapes
        self.i_grid:cq.Workplane|None = None
        self.power_greeble:cq.Workplane|None = None 
    
    def make_frame_power_greeble(self):
        if self.bp_power:
            bp_cap = self.bp_power
            diff = (self.length - self.base_length)/2 + self.side_inset/2
            
            bp_cap.length = diff-self.power_offset
            bp_cap.make()

            self.power_greeble = bp_cap.build().translate((
                self.length/2-bp_cap.length/2 - self.power_offset,
                0,
                -self.height/2+bp_cap.height/2
            ))
    
    def make_greebled_panel(self):
        i_grid = irregular_grid(
            length = self.length,
            width = self.height,
            height = (self.width/3)-4,
            max_height = (self.width/3),
            max_columns = self.max_columns,
            max_rows = self.max_rows,
            col_size = self.col_size,
            row_size = self.row_size,
            align_z = False,
            include_outline = True,
            passes_count = self.passes_count,
            seed = self.seed,
            make_item = None,
            union_grid = False,
        )
        self.i_grid = i_grid.rotate((1,0,0),(0,0,0),90)# = i_grid.translate((0,0,-1*(height/2)))
    
    def _make_center(self, width:float) -> cq.Workplane:
        mid_offset = self._calculate_mid_offset()
        center = shape.coffin(
            self.length,
            self.height,
            width,
            top_length = self.top_length,
            base_length = self.base_length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)
        
        center_cut = shape.coffin(
            self.length-(self.frame_size*2),
            self.height-(self.frame_size*2),
            self.width,
            top_length = self.top_length - self.frame_size,
            base_length = self.base_length - self.frame_size,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)
        
        center_frame = (
            cq.Workplane("XY")
            .union(center)
            .cut(center_cut)
        )
        
        if self.i_grid:
            center_frame = (
                center_frame
                .intersect(self.i_grid)
            )

        if self.power_greeble:
            self.power_greeble = self.power_greeble.cut(center_cut)
        
        return center_frame
    
    def _make_side(self, width:float) -> cq.Workplane:
        mid_offset = self._calculate_mid_offset()
        
        side = shape.coffin(
            self.length - self.side_inset,
            self.height - (self.side_inset/2),
            width,
            top_length = self.top_length - self.side_inset,
            base_length = self.base_length - self.side_inset,
            mid_offset = mid_offset + (self.side_inset/4)
        ).rotate((1,0,0),(0,0,0),-90)
        
        side_cut = self._make_side_cut(width = width)
        
        side_frame = (
            cq.Workplane("XY")
            .union(side)
            .cut(side_cut)
        )
        
        if self.i_grid:
            greebled_side_frame = (
                side_frame
                .intersect(self.i_grid)
                .union(side_frame.translate((0,-1.5,0)))
            )
            
        return greebled_side_frame
        
    def make(self, parent=None):
        self.parent = parent
        self.make_called = True

        self.make_frame_power_greeble()
        self.make_greebled_panel()
        self.make_frame()
        
    def build(self) -> cq.Workplane:
        if self.make_called == False:
            raise Exception('Make has not been called')
        
        scene = cq.Workplane("XY")
        
        if self.frame:
            scene = scene.union(self.frame)
        else:
            raise Exception('Unable to resolve frame')
        
        if self.power_greeble:
            scene = (
                scene
                .union(self.power_greeble)
                .union(self.power_greeble.rotate((0,0,1),(0,0,0),180))
            )
        
        return scene