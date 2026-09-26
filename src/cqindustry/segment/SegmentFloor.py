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
from cqterrain.floor import BaseFloor, TileFloor, FramedFloor

class SegmentFloor(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.length:float = 75
        self.width:float = 75
        self.height:float = 4
        self.top_padding:float = 1
        
        # blueprints
        self.bp_floor:BaseFloor = TileFloor()
        self.bp_frame:FramedFloor = FramedFloor()
        
        #shapes
        self.outline:cq.Workplane|None = None
        
    def make_outline(self):
        outline = cq.Workplane("XY").box(
            self.length,
            self.width,
            self.height
        )
        
        self.outline = outline
        
    def make_floor(self):
        if self.bp_floor:
            length = self.length
            width = self.width
            height = self.height
            
            self.bp_floor.length = length
            self.bp_floor.width = width
            self.bp_floor.height = height - self.top_padding
            self.bp_floor.make()
        
    def make_frame(self):
        if self.bp_frame:
            length = self.length
            width = self.width
            height = self.height
            
            self.bp_frame.length = length
            self.bp_frame.width = width
            self.bp_frame.height = height
            self.bp_frame.make()
        
    def make(self):
        super().make()
        self.make_outline()
        self.make_floor()
        self.make_frame()
        
    def build_outline(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.outline:
            part = part.add(self.outline)
        
        return part
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_frame:
            frame = self.bp_frame.build()
            z_translate = self.height / 2
            part = part.add(frame.translate((0,0,0)))
            
        if self.bp_floor:
            z_translate = self.height / 2
            frame_cut = self.bp_frame.frame_cut.translate((0,0,0))
            floor = self.bp_floor.build().intersect(frame_cut)
            part = part.union(floor.translate((0,0,-self.top_padding/2)))
        
        z_translate = self.height / 2
        return part.translate((0,0,-0))