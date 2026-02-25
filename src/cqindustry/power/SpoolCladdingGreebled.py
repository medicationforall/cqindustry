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
import math
from . import SpoolCladding
from cadqueryhelper.grid import irregular_grid

class SpoolCladdingGreebled(SpoolCladding):
    def __init__(self):
        super().__init__()
        self.seed:str = "test4"
    
    def __make_greebled_panel(self, length:float, width:float , height:float):    
        i_grid = irregular_grid(
            length = length,
            width = width,
            height = math.floor(height/2),
            max_height = height+1,
            col_size = 4,
            row_size = 3,
            align_z = True,
            include_outline = False,
            passes_count = 1000,
            seed = self.seed,
            make_item = None,
            union_grid = False,
        )
        return i_grid.translate((0,0,-1*(height/2)))
    
    def _make_clad(self, loc:cq.Location)->cq.Shape:
        length = self.parent.height - self.parent.wall_width*2 #type:ignore
        width = self.clad_width
        height = self.clad_height
        
        greebled_panel = self.__make_greebled_panel(length,width,height)
        
        clad = (
            cq.Workplane("XY")
            .union(greebled_panel)
            .rotate((0,1,0),(0,0,0), -90)
            .translate((-1*(height/2)-self.clad_inset,0,0))
        )
        
        return clad.val().located(loc) #type:ignore