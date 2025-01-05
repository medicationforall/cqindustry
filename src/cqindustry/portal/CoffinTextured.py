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
from . import BaseCoffin
from cadqueryhelper import irregular_grid

class CoffinTextured(BaseCoffin):
    def __init__(self):
        super().__init__()
        #parameters
        self.seed:str|None = 'rabblerabble'
        self.max_columns:int = 4
        self.max_rows:int = 2
        self.col_size:float = 15
        self.row_size:float = 15
        self.passes_count:int = 25
        
        #shapes
        self.texture:cq.Workplane|None = None

    def _make_texture(self):
        i_grid = irregular_grid(
            length = self.length,
            width = self.height,
            height = self.width/2,
            max_height = (self.width),
            max_columns = self.max_columns,
            max_rows =  self.max_rows,
            col_size = self.col_size,
            row_size = self.row_size,
            align_z = True,
            include_outline = False,
            passes_count = self.passes_count,
            seed = self.seed,
            make_item = None,
            union_grid = False,
        )
        self.texture = (
            i_grid
            .translate((0,0,-self.width))
            .rotate((1,0,0),(0,0,0),-90)
            .rotate((0,0,1),(0,0,0),180)
        )

    def make(self, parent=None):
        super().make(parent)
        self._make_texture()

    def build(self):
        base = super().build()

        if self.texture:
            scene = (
                cq.Workplane("XY")
                .union(base)
                .cut(self.texture)
            )
            
            return scene
        else:
            raise Exception("Unable to resolve generated texture")
