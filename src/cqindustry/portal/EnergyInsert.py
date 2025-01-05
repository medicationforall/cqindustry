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
from cadqueryhelper import Base, shape, randomized_rotation_grid
from cqterrain.damage import uneven_plane
from cqterrain.tile import truchet_circle_three
from typing import Tuple

class EnergyInsert(Base):
    def __init__(self):
        super().__init__()

        #parameters
        self.length:float = 150
        self.height:float = 150
        self.width:float = 5
        self.top_length:float = 90
        self.base_length:float = 100
        self.base_offset:float = 35
        self.base_height:float = 10
        self.uneven_plane_height:float = 4
        self.uneven_min_height:float = 0.25
        self.uneven_plane_seed:str|None = 'left'
        self.uneven_peak_count:int| Tuple[int, int] = (5,6)
        self.uneven_segments:int = 10
        self.uneven_spacer:float = 2.25
        self.uneven_step:float = .5
        self.uneven_plate_height:float = 0.25
        self.truchet_tolerance:float = 0.05
        self.truchet_seed:str|None = 'retro'
        self.debug_plane:bool = False
        self.render_truchet_grid:bool = True
        self.truchet_chamfer:float = .4

        #shapes
        self.window:cq.Workplane|None = None
        self.uneven_plane:cq.Workplane|None = None
        self.truchet_grid:cq.Workplane|None = None

    def _calculate_mid_offset(self) -> float:
        mid_offset = -1*(self.height/2) + self.base_offset
        return mid_offset

    def _make_window(self):
        mid_offset:float = self._calculate_mid_offset()
        
        length = self.length 
        width = self.width
        height = self.height
        top_length = self.top_length

        cut_out = shape.coffin(
            length,
            height,
            width,
            top_length,
            length,
            mid_offset = mid_offset
        ).rotate((1,0,0),(0,0,0),-90).translate((0,0,0))
        
        cut_combined = (
            cq.Workplane("XY")
            .union(cut_out.translate((0,0,self.height/2)))
            #.union(cut_base.translate((0,0,self.base_height/2)))
        )
        
        self.window = cut_combined
        
    def _make_uneven_plane(self):
        plate = uneven_plane(
            length = self.length, 
            width = self.height,
            segments = self.uneven_segments,
            height =  self.uneven_plane_height,
            min_height = self.uneven_min_height,
            step = self.uneven_step,
            peak_count = self.uneven_peak_count, 
            seed = self.uneven_plane_seed,
            render_plate = True,
            plate_height = self.uneven_plate_height
        )
        if self.debug_plane:
            scene = (
                cq.Workplane("XY")
                .union(self.window)
                .add(plate)
                
                .add(plate.rotate((1,0,0),(0,0,0),90).translate((0,-self.uneven_spacer,self.height/2+self.base_height)))
                .add(plate.rotate((1,0,0),(0,0,0),90).rotate((0,0,1),(0,0,0),180).translate((0,self.uneven_spacer,self.height/2+self.base_height)))
            )
        else:
            scene = (
                cq.Workplane("XY")
                .union(self.window)
                #.add(plate)
                
                .cut(plate.rotate((1,0,0),(0,0,0),90).translate((0,-self.uneven_spacer,self.height/2+self.base_height)))
                .cut(plate.rotate((1,0,0),(0,0,0),90).rotate((0,0,1),(0,0,0),180).translate((0,self.uneven_spacer,self.height/2+self.base_height)))
            )
        self.uneven_plane = scene
        
        
    def _make_truchet_grid(self):
        truchet_tile = truchet_circle_three(
            length=15,
            width=15,
            radius=2.5 
        )
        
        random_grid = randomized_rotation_grid(
            truchet_tile,
            x_spacing=15,
            y_spacing=15,
            x_count=10,
            y_count=10,
            seed = self.truchet_seed
        ).rotate((1,0,0),(0,0,0),90).translate((0,0,self.height/2+self.base_height))
        
        if self.window:
            i_random_grid = random_grid.intersect(
                self.window,
                clean=True,
                tol=self.truchet_tolerance
            )
            
            self.truchet_grid = i_random_grid
        #self.truchet_grid = truchet_tile

    def make(self, parent=None):
        super().make(parent)
        self._make_window()
        self._make_uneven_plane()

        if self.render_truchet_grid:
            self._make_truchet_grid()

    def build(self):
        super().build()
        scene = cq.Workplane("XY")
    
        if self.render_truchet_grid and self.truchet_grid:
            scene = scene.union(self.truchet_grid)
            scene = scene.faces("Y or -Y").chamfer(self.truchet_chamfer)
            
        if self.uneven_plane:
            scene = scene.union(self.uneven_plane)

        return scene