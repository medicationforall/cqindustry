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
from . import BaseHexagon, make_hexagon
from cadqueryhelper import series
import math

class VentHexagon(BaseHexagon):
    def __init__(self):
        super().__init__()
        self.radius:float = 58
        self.height:float = 4
        self.frame_size:float = 5
        self.vent_width:float = 2
        self.vent_space:float = 0.6
        self.vent_rotate:float = 45

        self.hexagon:cq.Workplane|None = None
        self.hexagon_cut:cq.Workplane|None = None
        self.vents:cq.Workplane|None = None

    def _calc_vent_size(self)-> int:
        return math.floor((self.radius - self.frame_size * 2) / (self.vent_space + self.vent_width))

    def __make_vents(self):
        vent = (
        cq.Workplane("XY")
            .box(self.radius - self.frame_size, self.vent_width , self.height)
            .rotate((1,0,0), (0,0,0), self.vent_rotate)
        )

        vent_size = self._calc_vent_size()

        self.vents = series(
            shape = vent,
            length_offset = None,
            width_offset = self.vent_space,
            height_offset = None,
            size = vent_size
        )

    def _calc_radius(self) -> float:
        radius = self.radius

        if self.parent and hasattr(self.parent, "hex_radius") and hasattr(self.parent, "hex_radius_cut"):
            radius = self.parent.hex_radius - self.parent.hex_radius_cut
        return radius

    def make(self,parent=None):
        super().make(parent)

        radius:float = self._calc_radius()

        self.hexagon = make_hexagon(radius, self.height, 0)
        self.hexagon_cut = make_hexagon(radius - self.frame_size, self.height, 0)
        self.__make_vents()


    def build(self)->cq.Workplane:
        super().build()
        scene = cq.Workplane("XY")

        if self.hexagon:
            scene = scene.union(self.hexagon)

        if self.hexagon_cut:
            scene = scene.cut(self.hexagon_cut)

        if self.vents and self.hexagon_cut:
            scene = scene.union(self.vents.intersect(self.hexagon_cut))

        return scene
    
    def build_assembly(self)->cq.Assembly:
        scene = self.build()

        assembly = cq.Assembly()
        assembly.add(scene,color=cq.Color(1,0,0), name="vent")
        return assembly