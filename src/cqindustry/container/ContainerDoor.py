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
from ..portal import BaseCoffin

class ContainerDoor(BaseCoffin):
    def __init__(self):
        super().__init__()

        #parameters
        self.cut_depth:float = 2
        self.padding:float = 3
        self.frame_width:float = 2
        self.x_translate:float = 0
        
        #shapes
        self.door_cut:cq.Workplane|None = None
        self.cross:cq.Workplane|None = None
        
    def __make_door_cut(self):
        self.door_cut = shape.coffin(
            self.length-self.padding*3,
            self.height-self.padding*2.5,
            self.cut_depth,
            self.top_length-self.padding*2,
            self.base_length -self.padding*2,
            -1*(self.height/2)+self.base_offset
        ).rotate((1,0,0),(0,0,0), -90)

    def make(self, parent = None):
        super().make(parent)
        self.__make_door_cut()
        
        result = shape.cross(
          length=self.length-self.padding,
          width=self.height,
          height=self.cut_depth,
          cross_length=self.frame_width,
          cross_width=self.frame_width,
          x_translate=self.x_translate,
          y_translate=-1*(self.height/2)+self.base_offset
        ).rotate((1,0,0),(0,0,0),-90)
        self.cross = result
        
    def build(self) -> cq.Workplane:
        if self.door_cut and self.cross:
            cut_frame = (
                cq.Workplane("XY")
                .add(self.door_cut)
                .cut(self.cross)
            ).faces("Y").edges().fillet(1.9)
            #return cut_frame
        
            scene = (
                cq.Workplane("XY")
                .add(super().build())
                .cut(cut_frame.translate((0,-1*(self.width/2)+self.cut_depth/2,0)))
            )
            return scene
        else:
            raise Exception('Could not resolve ContainerDoor door_cut or cross')