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
from . import BaseCoffin

class Ramp(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length:float = 150
        self.width:float = 10
        self.height:float = 150
        self.top_length:float = 90
        self.base_length:float = 100
        self.base_offset:float = 35 # offset distance from the base of the ramp

        self.side_inset:float = 8
        self.frame_size:float = 10
        self.inside_margin:float = 0.4

        self.render_outside:bool = True
        self.render_inside:bool = True
        
        #blueprints
        self.bp_outside = BaseCoffin()
        self.bp_inside = BaseCoffin()

    def __calculate_outside_length(self) -> float:
        return self.length - self.side_inset - (self.frame_size/2)
    
    def __calculate_outside_height(self)  -> float:
        return self.height - (self.side_inset/2) - (self.frame_size/2)
    
    def __calculate_outside_top_length(self) -> float:
        return self.top_length - self.side_inset - (self.frame_size/2)
    
    def __calculate_outside_base_length(self) -> float:
        return self.base_length - self.side_inset - (self.frame_size/2)

    def __calculate_inside_length(self) -> float:
        return self.length -(self.frame_size*2) - self.side_inset - self.inside_margin*2
    
    def _calculate_inside_height(self) -> float:
        return self.height -(self.frame_size*2) - self.side_inset/2 - self.inside_margin*2
    
    def __calculate_inside_top_length(self) -> float:
        return self.top_length - self.frame_size - self.side_inset - self.inside_margin
    
    def __calculate_inside_base_length(self) -> float:
        return self.base_length - self.frame_size - self.side_inset - self.inside_margin
    
    def _calculate_max_inside_length(self) -> float:
        length = self.__calculate_inside_length()
        top_length = self.__calculate_inside_top_length()
        base_length = self.__calculate_inside_base_length()
        if top_length > length:
            length = top_length
            
        if base_length > length:
            length = base_length
        return length
    
    def __make_inside(self):
        self.bp_outside.length = self.__calculate_outside_length()
        self.bp_outside.width = self.width / 2
        self.bp_outside.height = self.__calculate_outside_height()
        self.bp_outside.top_length = self.__calculate_outside_top_length()
        self.bp_outside.base_length = self.__calculate_outside_base_length()
        self.bp_outside.base_offset = self.base_offset # offset distance from the center of the ramp
        self.bp_outside.make(self)
        
    def __make_outside(self):
        self.bp_inside.length = self.__calculate_inside_length()
        self.bp_inside.width = self.width / 2
        self.bp_inside.height = self._calculate_inside_height()
        self.bp_inside.top_length = self.__calculate_inside_top_length()
        self.bp_inside.base_length = self.__calculate_inside_base_length()
        
        height_diff = (self.height - self._calculate_inside_height())/2
        self.bp_inside.base_offset = self.base_offset -height_diff + self.side_inset /4
        self.bp_inside.make(self)
        
    def make(self, parent=None):
        super().make(parent)

        if self.parent:
            #self.parent.make()

            self.length = self.parent.length
            self.height = self.parent.height
            self.top_length = self.parent.top_length
            self.base_length = self.parent.base_length
            self.base_offset = self.parent.base_offset
            self.frame_size = self.parent.frame_size
            self.side_inset = self.parent.side_inset

        self.__make_inside()
        self.__make_outside()

    def build(self) -> cq.Workplane:
        super().build()
        outside = self.bp_outside.build()
        inside = self.bp_inside.build()
        
        side_inset = self.side_inset
        frame_size = self.frame_size/2
        out_z = -1*(side_inset/4+frame_size/2)
        in_z = -1*(self.side_inset/4)

        ramp = (
            cq.Workplane("XY")
        )

        if self.render_inside:
            ramp = ramp.add(inside.translate((0,self.width/4,in_z)))

        if self.render_outside:
            ramp = ramp.add(outside.translate((0,-self.width/4,out_z)))

        return ramp