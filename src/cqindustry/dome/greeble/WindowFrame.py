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
from . import make_hexagon, make_pentagon, CutKeyHexagon, CutKeyPentagon
from cadqueryhelper import Base
from typing import Literal

_types = {
    'hexagon':make_hexagon, 
    'pentagon':make_pentagon
}

_key_classes = {
    "hexagon":CutKeyHexagon, 
    "pentagon":CutKeyPentagon
}

class WindowFrame(Base):
    def __init__(self):
        super().__init__()
        self.type:Literal["hexagon", "pentagon"] = "hexagon" # hexagon, pentagon
        self.radius:float = 58
        self.height:float = 4
        self.margin:float = 0 # used when determing outside radius
    
        self.pane_height:float = 1 # internal cut height
        self.inner_pane_padding:float = 2
        self.pane_rail_translate:float = 0 
        self.frame_size:float = 5

        self.render_pane:bool = False

        self.outline:cq.Workplane|None = None
        self.pane_rail:cq.Workplane|None = None
        self.frame:cq.Workplane|None = None
        self.cut_key_bp = None

    def _calc_radius(self) -> float:
        radius = self.radius

        if self.type == "pentagon" and self.parent and hasattr(self.parent, "pen_radius") and hasattr(self.parent, "pen_radius_cut"):
            radius = self.parent.pen_radius - self.parent.pen_radius_cut - self.margin
        elif self.type == "hexagon" and self.parent and hasattr(self.parent, "hex_radius") and hasattr(self.parent, "hex_radius_cut"):
            radius = self.parent.hex_radius - self.parent.hex_radius_cut - self.margin
        return radius


    def _resolve_make_method(self):
        if(self.type in _types):
            return _types[self.type]
        else:
            raise Exception(f'unknown make method type {self.type}')


    def __make_frame(self):
        radius = self._calc_radius()
        make_method = self._resolve_make_method()
        
        self.outline = make_method(radius, self.height,0)
        cut_frame = make_method(radius - self.frame_size, self.height,0)
        self.frame = self.outline.cut(cut_frame)
        
    def __make_pane_rail(self):
        radius = self._calc_radius()
        make_method = self._resolve_make_method()
        
        pane = make_method(radius, self.pane_height,0)
        inner_pane = make_method(
            radius - self.frame_size + self.inner_pane_padding, 
            self.pane_height, 
            0
        )
        pane_cut = (
            cq.Workplane("XY").box(radius, radius, self.pane_height)
            .translate((-1*(radius/2)+self.pane_rail_translate,0,0))
        )
        
        self.pane_rail = (
            pane
            .cut(pane_cut)
            .union(inner_pane)
        )


    def __make_cut_key(self):
        inner_radius = self._calc_radius() - self.frame_size + (self.inner_pane_padding/2)
        
        if self.type in _key_classes:
            self.cut_key_bp = _key_classes[self.type]()
        else:
            raise Exception(f"Unknown type {self.type}")

        self.cut_key_bp.radius = inner_radius
        #self.cut_key_bp.height = self.height
        self.cut_key_bp.text = f" {self.type[:3]} Key"
        self.cut_key_bp.make()


    def make(self, parent=None):
        super().make(parent)
        self.__make_frame()
        self.__make_pane_rail()
        self.__make_cut_key()


    def build(self)->cq.Workplane:
        super().build()
        window = cq.Workplane("XY")

        if self.frame:
            window = window.union(self.frame)

        if self.pane_rail:
            window = window.cut(self.pane_rail)

            if self.render_pane:
                 window = window.add(self.pane_rail)
        return window
    
    def build_assembly(self)->cq.Assembly:
        assembly = cq.Assembly()

        window = cq.Workplane("XY")

        if self.frame:
            window = window.union(self.frame)

        if self.pane_rail:
            window = window.cut(self.pane_rail)

        assembly.add(window,color=cq.Color(1, 0, 0), name="window_frame")

        if self.render_pane:
            assembly.add(self.pane_rail ,color=cq.Color(0, 1, 0), name="window_pane_rail")

        return assembly