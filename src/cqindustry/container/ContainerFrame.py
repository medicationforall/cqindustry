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
from ..portal import Frame

class ContainerFrame(Frame):
    def __init__(self):
        super().__init__()
        
    def make_frame(self):
        #log('make_frame_override')
        center = self._make_center(self.width/5)
        side = self._make_side(self.width/5)
        
        center_y = self.width/5
        frame = (
            cq.Workplane("XY")
            .union(center.translate((0,center_y,0)))
            .union(center.translate((0,-center_y,0)))
        )
        
        if self.render_sides:
            side_z = -1*(self.side_inset/4)
            side_y = self.width/5
            frame = (
                frame
                .union(side.translate((0,side_y*2,side_z)))
                .union(side.translate((0,0,side_z)))
                .union(side.translate((0,-side_y*2,side_z)))
            )
        
        self.frame = frame
        
    def make(self, parent=None):
        super().make(parent)
            
    def build(self) -> cq.Workplane:
        return super().build()