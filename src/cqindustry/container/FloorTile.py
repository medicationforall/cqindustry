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
import math
from . import Floor
from typing import Callable

def make_basic_tile(
    length:float, 
    width:float, 
    height:float
) -> cq.Workplane:
    tile = cq.Workplane("XY").box(
        length, 
        width, 
        height
    )
    return tile

class FloorTile(Floor):
    def __init__(self):
        super().__init__()

        #propertes
        self.tile_length:float = 10
        self.tile_width:float = 10
        self.tile_padding:float = 1
        self.make_tile_method:Callable[[float, float, float], cq.Workplane] = make_basic_tile
        
    def _make_floor(self):
        if not self.make_tile_method:
            raise Exception("Missing make_tile_method callback")
        else:
            tile = self.make_tile_method(self.tile_length, self.tile_width, self.height)
        
        tile_length = self.tile_length + self.tile_padding * 2
        tile_width = self.tile_width + self.tile_padding * 2
        
        x_count = math.floor(self.length / tile_length)
        y_count = math.floor(self.width / tile_width)

        def add_tile(loc:cq.Location) -> cq.Shape:
            return tile.val().located(loc) #type: ignore
        
        result = (
            cq.Workplane("XY")
            .rarray(
                xSpacing = tile_length, 
                ySpacing = tile_width,
                xCount = x_count, 
                yCount= y_count, 
                center = True)
            .eachpoint(callback = add_tile)
        )

        self.floor = result

    def make(self, parent = None):
        super().make(parent)
    
    def build(self) -> cq.Workplane:
        return super().build()