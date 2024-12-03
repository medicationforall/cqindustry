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
from cadqueryhelper import Base
from .greeble import make_hexagon, make_pentagon

def _rotate(shape:cq.Workplane, x_rotate:float=0, z_rotate:float=0):
    if shape:
        shape = (
            cq.Workplane("XY")
            .union(shape) #clone the shape
            .rotate((0,0,1),(0,0,0),z_rotate)
            .rotate((1,0,0),(0,0,0),x_rotate)
        )
    return shape


class Dome(Base):
    def __init__(self):
        super().__init__()
        self.hex_radius:float = 58
        self.hex_pen_diff:float = 7
        self.hex_height:float = 4
        self.hex_radius_cut:float = 9

        self.pen_radius:float = self.hex_radius - self.hex_pen_diff
        self.pen_radius_cut:float = 10

        # rotates
        self.r1_x_rotate:float = 32

        self.r2_x_rotate:float = -58
        self.r2_z_rotate:float = 30

        self.r2_pen_x_rotate:float = 63
        self.r2_pen_z_rotate:float = 54

        self.r3_x_rotate:float = 92
        self.r3_z_rotate:float = 30

        # greebles
        self.greebles_bp = []

        # render flags
        self.render_frame:bool = True
        self.render_greebles:bool = True

        #--- shapes
        self.pentagon:cq.Workplane|None = None
        self.pentagon_cut:cq.Workplane|None = None
        self.hexagon:cq.Workplane|None = None
        self.hexagon_cut:cq.Workplane|None = None
        self.box_cut:cq.Workplane|None = None


    def make(self, parent=None):
        super().make(parent)
        self.__make_base_shapes()
        self.box_cut = cq.Workplane("XY").box(153,160,150)

        for bp in self.greebles_bp:
            if bp and bp.make:
                bp.make(self)


    def __make_base_shapes(self):
        self.pentagon = make_pentagon(self.pen_radius, self.hex_height, 0)
        self.hexagon = make_hexagon(self.hex_radius, self.hex_height, 0)

        self.pentagon_cut = make_pentagon(
            self.pen_radius - self.pen_radius_cut,
            self.hex_height,
            0
        )
        self.hexagon_cut = make_hexagon(
            self.hex_radius - self.hex_radius_cut,
            self.hex_height,
            0
        )


    def build(self)->cq.Workplane:
        super().build()
        
        if self.render_frame:
            dome = self.build_frame()
        else:
            dome = cq.Workplane("XY")
        greebled_r1 = None
        greebled_r2 = None

        #greebles

        ## center greeble
        if self.render_greebles:
            if self.greebles_bp and len(self.greebles_bp) > 0:

                hexes_bp = None
                center_pentagon = None
                if self.greebles_bp[0] and self.greebles_bp[0].build:
                    center_pentagon = self.greebles_bp[0].build()

                if len(self.greebles_bp) > 1:
                    hexes_bp = self.greebles_bp[1:6]

                greebled_r1 = self.__build_ring1_list(
                    hexes_bp,
                    center_pentagon
                )

            pentagons_bp = None
            hexagons_bp = None
            if len(self.greebles_bp) > 6:
                pentagons_bp = self.greebles_bp[6::2]

            if len(self.greebles_bp) > 6:
                hexagons_bp = self.greebles_bp[7::2]

            if pentagons_bp or hexagons_bp:
                #print(f'pentagons_bp {pentagons_bp}, hexagons_bp {hexagons_bp}')
                greebled_r2 = self.__build_ring2_list(
                    hexagons_bp,
                    pentagons_bp,
                )


        if greebled_r1:
            dome = dome.add(greebled_r1.translate((0,0,60)))

        if greebled_r2:
            dome = dome.add(greebled_r2.translate((0,0,60)))

        return dome


    def build_frame(self):
        dome = cq.Workplane("XY")

        if self.hexagon and self.pentagon:
            solid_dome = self.__build_ring1(self.hexagon, self.pentagon)
            ring_2 = self.__build_ring2(self.hexagon, self.pentagon)
            ring_3 = self.__build_ring_3(self.hexagon)

        if self.hexagon_cut and self.pentagon_cut:
            cut_dome = self.__build_ring1(self.hexagon_cut, self.pentagon_cut)
            ring_2_cut = self.__build_ring2(self.hexagon_cut, self.pentagon_cut)
        

        dome = (
            dome
            .union(solid_dome)
            .union(ring_2)
            .union(ring_3.translate((0,0,-60)).rotate((0,0,1),(0,0,0),18))
            .cut(cut_dome)
            .cut(ring_2_cut)
        )

        if self.box_cut:
            dome = (
                dome
                .translate((0,0,60))
                .cut(self.box_cut.translate((0,0,-1*(150/2))))
            )

        return dome


    def __build_ring1(self, hex_shape:cq.Workplane, pen_shape:cq.Workplane, keep_hex=None):
        h =  _rotate(hex_shape,self.r1_x_rotate,0)
        p =  _rotate(pen_shape,0,0)
        dome = (
            cq.Workplane("XY")
        )

        #center
        if p:
            dome = dome.union(
                p
                .translate((0,0,12.2))
                .rotate((0,0,1),(0,0,0),18)
            )

        #ring 1
        if h:
            for i in range(5):
                if keep_hex == None or i in  keep_hex:
                    dome = (
                        dome
                        .union(
                            h
                            .translate((0,38.5,0))
                            .rotate((0,0,1),(0,0,0), 72*i)
                        )
                    )

        return dome

    def __build_ring1_list(self, hex_list, pen_shape:cq.Workplane|None):
        dome = (
            cq.Workplane("XY")
        )

        #center
        if pen_shape:
            dome = dome.union(
                pen_shape
                .translate((0,0,12.2))
                .rotate((0,0,1),(0,0,0),18)
            )

        #ring 1
        if hex_list:
            for i in range(5):
                try:
                    node = hex_list[i]
                    if node:
                        h = node.build()
                        h =  _rotate(h,self.r1_x_rotate,0)
                        dome = (
                            dome
                            .union(
                                h
                                .translate((0,38.5,0))
                                .rotate((0,0,1),(0,0,0), 72*i)
                            )
                        )
                except IndexError:
                    print("Index doesn't exist!")
        return dome


    def __build_ring2(self, hex_shape:cq.Workplane, pen_shape:cq.Workplane, keep_hex = None, keep_pen = None):
        h =  _rotate(hex_shape,self.r2_x_rotate,self.r2_z_rotate)
        p =  _rotate(pen_shape,self.r2_pen_x_rotate,self.r2_pen_z_rotate)
        r2_p_y = 65.6
        ring = (
            cq.Workplane("XY")
        )

        if h:
            for i in range(5):
                if keep_hex == None  or i in  keep_hex:
                    ring = (
                        ring
                        .union(
                            h
                            .translate((0,-61.5,-23))
                            .rotate((0,0,1),(0,0,0),72*i)
                        )
                    )
        if p:
            for i in range(5):
                if keep_pen == None  or i in  keep_pen:
                    ring = (
                        ring
                        .union(
                            p
                            .translate((0,r2_p_y,-28.3))
                            .rotate((0,0,1),(0,0,0),72*i)
                        )
                    )

        return ring

    def __build_ring2_list(self, hex_list, pen_list):
        r2_p_y = 65.6
        ring = (
            cq.Workplane("XY")
        )

        if hex_list:
            for i in range(5):
                try:
                    node = hex_list[i]
                    if node:
                        h = node.build()
                        h = _rotate(h,self.r2_x_rotate,self.r2_z_rotate)
                        ring = (
                            ring
                            .union(
                                h
                                .translate((0,-61.5,-23))
                                .rotate((0,0,1),(0,0,0),(72*i)+72*2)
                            )
                        )
                except IndexError:
                    print("Index doesn't exist!")

        if pen_list:
            for i in range(5):
                try:
                    node = pen_list[i]
                    if node:
                        p = node.build()
                        p =  _rotate(p,self.r2_pen_x_rotate,self.r2_pen_z_rotate)
                        ring = (
                            ring
                            .union(
                                p
                                .translate((0,r2_p_y,-28.3))
                                .rotate((0,0,1),(0,0,0),(72*i)-72*1)
                            )
                        )
                except IndexError:
                    print("Index doesn't exist!")

        return ring


    def __build_ring_3(self, hex_shape:cq.Workplane):
        h =  _rotate(hex_shape,self.r3_x_rotate,self.r3_z_rotate)
        r3_y=-73
        r3_z=-1
        ring_3 = (cq.Workplane("XY"))

        for i in range(10):
            ring_3 = (
                ring_3
                .union(
                    h
                    .translate((0,r3_y,r3_z))
                    .rotate((0,0,1),(0,0,0),36*i)
                )
            )
        return ring_3
