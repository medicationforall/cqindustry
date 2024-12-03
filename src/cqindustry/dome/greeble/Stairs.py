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
from . import make_angled_steps
from cadqueryhelper import Base

class Stairs(Base):
    def __init__(self):
        super().__init__()
        self.stairs = None
        self.display_dome = False
        
    def make(self, parent:Base|None=None):
        super().make(parent)
        
        if parent:
            parent.make()
            
        side_steps = make_angled_steps(width=10)
        side_cut = make_angled_steps(30-4,10)
        steps = make_angled_steps(30-4,10, 15-2)
        
        sides = (
            side_steps
            .cut(side_cut.translate((0,-.8,0)))
            .union(steps.translate((0,-.8,-1)))
        )
        
        self.stairs = sides
        
    def build(self):
        super().build()
        scene = cq.Workplane("XY")

        if self.stairs:
            scene = scene.add(self.stairs.translate((0,-83,15/2)))
        
        if self.parent:
            dome = self.parent.build()
            if self.display_dome:
                scene = scene.add(dome)
            else:
                scene = scene.cut(dome)

        return scene
    
    def build_assembly(self)->cq.Assembly:
        scene = self.build()

        assembly = cq.Assembly()
        assembly.add(scene,color=cq.Color(1,0,0), name="stairs")
        return assembly