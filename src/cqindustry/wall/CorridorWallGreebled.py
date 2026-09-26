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
from cqterrain.wall import BaseWall
from . import CorridorWall

class CorridorWallGreebled(Base):
    def __init__(self):
        #parameters        
        self.length:float = 75
        self.width:float = 12
        self.height:float = 75
        self.window_y_translate:float = 4
        self.window_z_translate:float = 0
        self.window_z_rotate:float|None = None
        
        #blueprints
        self.bp_wall:BaseWall = CorridorWall()
        self.bp_window:Base|None = None
        
    def make_wall(self):
        if self.bp_wall:
            length = self.length
            width = self.width
            height = self.height
            
            self.bp_wall.length = length
            self.bp_wall.width = width
            self.bp_wall.height = height
            self.bp_wall.make()
            
    def make_window(self):
        if self.bp_window:
            self.bp_window.make()
        
    def make(self):
        super().make()
        self.make_wall()
        self.make_window()
        
    def build(self)->cq.Workplane:
        super().build()
        
        part = cq.Workplane("XY")
        
        if self.bp_wall:
            wall = self.bp_wall.build()
            part = part.add(wall)
            
        if self.bp_window:
            window  = self.bp_window.build()
            if self.window_z_rotate:
                window = window.rotate((0,0,1),(0,0,0),self.window_z_rotate)

            cut_window = self.bp_window.build_outline()
            if self.window_z_rotate:
                cut_window = cut_window.rotate((0,0,1),(0,0,0),self.window_z_rotate)
            
            y_translate = self.window_y_translate
            z_translate = self.window_z_translate
            part = part.cut(cut_window.translate((0,y_translate,z_translate)))
            part = part.add(window.translate((0,y_translate,z_translate)))
            
        return part