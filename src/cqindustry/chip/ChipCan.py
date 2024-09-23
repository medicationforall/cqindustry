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
from cadqueryhelper import Base

class ChipCan(Base):
    def __init__(self):
        super().__init__()
        
        # parameters
        self.height:float = 75 * 3
        self.diameter:float = 75
        
        #shape
        self.can_cylinder:cq.Workplane|None = None
        
    def _make_can(self):
        radius = self.diameter / 2
        can = (
            cq.Workplane("XY")
            .cylinder(self.height, radius)
        )
        
        self.can_cylinder = can
        
    def make(self, parent = None):
        super().make(parent)
        self._make_can()
        
    def build(self) -> cq.Workplane:
        super().build()
        scene = cq.Workplane()

        if self.can_cylinder:
            scene = scene.union(self.can_cylinder)
        return scene