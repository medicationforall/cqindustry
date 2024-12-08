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
from cqterrain import pipe
from cadqueryhelper import Base

class Cradle(Base):
    def __init__(
            self, 
            length:float = 150,
            width:float = 75,
            height:float = 60,
            angle:float = 45
        ):
        super().__init__()
        #parameters
        self.length:float = length
        self.width:float = width
        self.height:float = height
        self.angle:float = angle
        self.spool_padding:float = 2
        
        self.cut_side_width:float = 3
        self.cut_side_padding:float = 3
        
        #shapes
        self.cradle:cq.Workplane|None = None
        self.cut_side:cq.Workplane|None = None
        self.power_line:cq.Workplane|None = None
        
    def __make_cradle(self):
        cradle = (
            cq.Workplane("XY")
            .sketch()
            .trapezoid(self.length,self.height,self.angle)
            .finalize()
            .extrude(self.width)
            .translate((0,0,-1*(self.width/2)))
            .rotate((1,0,0),(0,0,0),-90)
        )
        
        self.cradle = cradle
        
    def __make_cut_side(self):
        cut_side = (
            cq.Workplane("XY")
            .sketch()
            .trapezoid(self.length-self.cut_side_padding*5,self.height - self.cut_side_padding*2,self.angle)
            .finalize()
            .extrude(self.cut_side_width)
            .translate((0,0,-1*(self.cut_side_width/2)))
            .rotate((1,0,0),(0,0,0),-90)
        )
        self.cut_side = cut_side
        
    def __make_power_line(self):
        power_line =(
            pipe.straight(self.width)
            .rotate((0,0,1),(0,0,0),90)
        )
        self.power_line = power_line
        
        
    def make(self, parent=None):
        super().make(parent)
        if self.parent:
            self.parent.make()
        self.__make_cradle()
        self.__make_cut_side()
        self.__make_power_line()
        
    def build(self):
        super().build()
        #log(self.cut_side)
        cut_y_translate = self.width/2 - self.cut_side_width/2
        scene = cq.Workplane("XY")

        if self.cradle and self.cut_side:
            scene = (
                scene
                .union(self.cradle.translate((0,0,self.height/2))) 
                .cut(self.cut_side.translate((0,cut_y_translate,self.height/2)))
                .cut(self.cut_side.translate((0,-1*(cut_y_translate),self.height/2)))
            )
        
        if self.power_line:
            scene = (
                scene
                .union(self.power_line.translate((self.length/4,0,0)))
                .union(self.power_line.translate((-1*(self.length/4),0,0)))
            )
            
        if self.parent:
            cut_spool = (
                self.parent.build_no_center()
                .rotate((1,0,0),(0,0,0),90)
                .translate((0,0,self.parent.radius))
            )
            scene = scene.cut(cut_spool.translate((0,0,self.spool_padding)))

       # return self.cut_side
        return scene.translate((0,0,-1*(self.height/2)))