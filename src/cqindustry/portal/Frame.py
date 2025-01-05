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
from cadqueryhelper import Base, shape

class Frame(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.length:float = 150
        self.width:float = 15
        self.height:float = 150
        self.top_length:float = 90 # length at the top of the frame
        self.base_length:float = 100 # length at the base of the frame
        self.base_offset:float = 35 # offset distance from the center of the frame
        self.side_inset:float = 8 # The amount the inset the side frames in relation to the center.
        self.frame_size:float = 10 # distance from the outside wall and the inside wall.
        self.render_sides:bool = True
        
        # shapes
        self.frame:cq.Workplane|None = None

    def _calculate_mid_offset(self) -> float:
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset
    
    def _make_side_cut(self, width:float|None = None, margin:float = 0) -> cq.Workplane:
        mid_offset = self._calculate_mid_offset()
        if not width:
            width = self.width/3

        side_cut:cq.Workplane = shape.coffin(
            self.length-(self.frame_size*2) - self.side_inset - margin*2,
            self.height-(self.frame_size*2) - self.side_inset/2 - margin*2,
            width,
            top_length = self.top_length - self.frame_size - self.side_inset - margin,
            base_length = self.base_length - self.frame_size - self.side_inset - margin,
            mid_offset = mid_offset  + self.side_inset /4
        ).rotate((1,0,0),(0,0,0),-90)
        return side_cut
    
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
            width,
            top_length = self.top_length - self.frame_size,
            base_length = self.base_length - self.frame_size,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)
        
        center_frame = (
            cq.Workplane("XY")
            .union(center)
            .cut(center_cut)
        )
        
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
        
        return side_frame
        
    def make_frame(self):
        center = self._make_center(self.width/3)
        side = self._make_side(self.width/3)
        
        frame = (
            cq.Workplane("XY")
            .union(center)
        )
        
        if self.render_sides:
            side_z = -1*(self.side_inset/4)
            frame = (
                frame
                .union(side.translate((0,self.width/3,side_z)))
                .union(side.rotate((0,0,1),(0,0,0),180).translate((0,-1*(self.width/3),side_z)))
            )
        
        self.frame = frame
        
    def make(self, parent=None):
        super().make(parent)
        self.make_frame()
        
    def build(self) -> cq.Workplane:
        super().build()

        if self.frame:
            return self.frame
        else:
            raise Exception('Unable to resolve frame')