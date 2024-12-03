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

def _check_chamfer(height, chamfer):
    if not (chamfer < height):
        raise Exception(f"chamfer \"{chamfer}\" greater than or equal to height provided \"{height}\"")


class DoorHexagon(BaseHexagon):
    def __init__(self):
        super().__init__()
        self.radius:float = 58
        self.height:float = 4

        self.frame_inset:float = 4

        # door
        self.door_padding:float = .5
        self.door_chamfer:float = 1.5
        self.door_height:float = 4

        #hinge
        self.hinge_length:float = 4
        self.hinge_width:float = 16
        self.hinge_height:float = 5
        self.hinge_cylinder_height:float = 20
        self.hinge_cylinder_radius:float = 2.5
        self.hinge_x_translate:float = -4.3 #-3.5

        # handle
        self.handle_x_translate:float = 8.5
        self.handle_length:float = 5
        self.handle_width:float = 7

        # parts
        self.hexagon:cq.Workplane|None = None
        self.hexagon_cut:cq.Workplane|None = None
        self.frame:cq.Workplane|None = None
        self.hinge:cq.Workplane|None = None
        self.door_body:cq.Workplane|None = None
        self.handle_outline:cq.Workplane|None = None
        self.handle_detail:cq.Workplane|None = None


    def _calc_radius(self)->float:
        radius = self.radius

        if self.parent and hasattr(self.parent, "hex_radius") and hasattr(self.parent, "hex_radius_cut"):
            radius = self.parent.hex_radius - self.parent.hex_radius_cut
            #print(f'door _calc_radius set calculated radius {radius}, {self.parent.hex_radius}, {self.parent.hex_radius_cut}')
        return radius

    def make(self,parent=None):
        super().make(parent)

        radius = self._calc_radius()
        cut_radius = radius - self.frame_inset

        self.hexagon = make_hexagon(radius, self.height, 30)
        self.hexagon_cut = make_hexagon(cut_radius, self.height, 30)
        self.__make_frame()
        self.__make_door_body()
        self.__make_hinge()
        self.__make_handle()


    def __make_frame(self):
        self.frame = (
            cq.Workplane("XY")
            .union(self.hexagon)
        )

        if self.hexagon_cut:
            self.frame = self.frame.cut(self.hexagon_cut)

    def __make_door_body(self):
        radius = self._calc_radius()
        _check_chamfer(self.door_height/2, self.door_chamfer)
        door_radius = radius - (self.frame_inset - self.door_padding)
        door = (
            make_hexagon(door_radius, self.door_height, 30)
            .chamfer(self.door_chamfer)
        )

        self.door_body = door

    def __make_hinge(self):
        hinge_box = (
            cq.Workplane("XY")
            .box(self.hinge_length, self.hinge_width, self.hinge_height)
        )

        hinge_cylinder = (
            cq.Workplane("XY")
            .cylinder(self.hinge_cylinder_height,self.hinge_cylinder_radius)
            .rotate((1,0,0),(0,0,0),90)
        )

        self.hinge = (
            cq.Workplane("XY")
            .union(hinge_box)
            .union(hinge_cylinder.translate((-1,0,0)))
        ).translate((0.5,0,0))


    def __make_handle(self):
        self.handle_outline = (
            cq.Workplane("XY")
            .box(5,7,5.5)
            #.translate((16,0,0))
        )

        handle = cq.Workplane("XY").box(self.handle_length, self.handle_width,self.door_height+1.5)
        handle_cut = cq.Workplane("XY").box(self.handle_length-2,self.handle_width-3,self.door_height+2)
        handle_interier = cq.Workplane("XY").box(self.handle_length,self.handle_width,self.door_height-1)

        handle_detail = (
            handle
            .cut(handle_cut)
            .add(handle_interier)
            #.translate((16,0,0))
        )
        self.handle_detail = handle_detail


    def build(self) -> cq.Workplane:
        super().build()
        radius = self._calc_radius()
        cut_radius = radius - self.frame_inset
        assembly = (
            cq.Workplane("XY")
        )

        if self.frame:
            assembly = assembly.union(self.frame)

        if self.door_body:
            assembly = assembly.union(self.door_body)

        if self.hinge:
            assembly = assembly.union(
                self.hinge
                .translate((-1*(cut_radius/2) - self.hinge_x_translate,0,0))
            )
        if self.handle_outline:
            assembly = assembly.cut(self.handle_outline.translate(((cut_radius/2) - self.handle_x_translate,0,0)))

        if self.handle_detail:
            assembly = assembly.union(self.handle_detail.translate(((cut_radius/2) - self.handle_x_translate,0,0)))

        return assembly.rotate((0,0,1),(0,0,0), -30)
    
    def build_assembly(self)->cq.Assembly:
        scene = self.build()

        assembly = cq.Assembly()
        assembly.add(scene,color=cq.Color(1,0,0), name="door_hexagon")
        return assembly
