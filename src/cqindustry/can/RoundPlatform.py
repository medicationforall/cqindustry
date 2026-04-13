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
from cadqueryhelper.shape import cylinder_sector

class RoundPlatform(Base):
    def __init__(self):
        super().__init__()
        #parameters
        self.inner_diameter:float = 30
        self.outer_diameter:float = 55
        self.height:float = 4
        self.angle:float = 90
        
        #shapes
        self.outline:cq.Workplane|None = None
        self.platform:cq.Workplane|None = None
        
    def make_outline(self):
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
        
        self.outline = ex_platform
        
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
        
    def make(self):
        super().make()
        self.make_outline()
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
        
        if self.outline:
            part = part.add(self.outline)
        
        return part