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
from cadqueryhelper import Base

class SpoolCladding(Base):
    def __init__(
            self,
            start_angle:float = 0,
            end_angle:float = 360,
            rotate_solid:bool = True,
            count:int = 17,
            clad_width:float = 33,
            clad_height:float = 5,
            clad_inset:float = 5
        ):
        super().__init__()
        
        #arc parameters
        self.start_angle:float = start_angle
        self.end_angle:float = end_angle
        self.rotate_solid:bool = rotate_solid
        self.count:int = count
        
        #clad
        self.clad_height:float = clad_height
        self.clad_width:float = clad_width
        self.clad_inset:float = clad_inset
        
        # parts 
        self.cladding:cq.Workplane|None = None
        
    def _make_clad(self, loc:cq.Location)->cq.Shape:
        length = self.parent.height - self.parent.wall_width*2 #type:ignore
        width = self.clad_width
        height = self.clad_height
        clad = (
            cq.Workplane("XY").box(length,width,height)
            .rotate((0,1,0),(0,0,0), 90)
            .translate((-1*(height/2)-self.clad_inset,0,0))
        )
        return clad.val().located(loc) #type:ignore
    
    def __make_cladding(self):
        cladding_arc =(
            cq.Workplane("XY")
            .polarArray(
                radius  = self.parent.radius, #type:ignore
                startAngle  = self.start_angle, 
                angle  = self.end_angle, 
                count  = self.count,
                fill = True,
                rotate = self.rotate_solid
            )
            .eachpoint(callback = self._make_clad)
        )
        
        self.cladding = cladding_arc
        
    def make(self, parent = None):
        super().make(parent)
        self.__make_cladding()

        
    def build(self) -> cq.Workplane:
        super().build()
        scene = cq.Workplane("XY")

        if self.cladding:
            scene = scene.union(self.cladding)
        
        return scene