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

class BaseCoffin(Base):
    def __init__(self):
        super().__init__()
        self.length:float = 150
        self.width:float = 5
        self.height:float = 150
        self.top_length:float = 90 # Length at the top of the shape
        self.base_length:float = 100 # Length at the base of the shape
        self.base_offset:float = 35 # offset distance from the base of the shape

        # shapes
        self.coffin:cq.Workplane|None = None

    def _calculate_mid_offset(self) -> float:
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset  
    
    def make(self, parent=None):
        super().make(parent)

        mid_offset = self._calculate_mid_offset()
        coffin = shape.coffin(
            self.length,
            self.height,
            self.width,
            self.top_length,
            self.base_length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90)

        self.coffin = coffin

    def build(self) -> cq.Workplane:
        super().build()

        if self.coffin:
            return self.coffin
        else:
            raise Exception('Unable to resolve Base shape')
