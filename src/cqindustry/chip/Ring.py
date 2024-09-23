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
from cadqueryhelper import Base, shape
from cqterrain import Ladder

class Ring(Base):
    def __init__(self):
        super().__init__()

        # parameters
        self.cut_diameter:float = 76
        self.diameter:float = self.cut_diameter + 10
        self.inset:float = 5
        self.height:float = 10

        self.render_ladders:bool = True
        self.ladder_height:float = 71
        self.ladder_length:float = 25
        self.ladder_width:float = 10
        self.ladder_cut_padding:float = 1.5
        self.ladder_cut_chamfer:float = 2

        # shapes
        self.ring:cq.Workplane|None = None
        self.cut_ladders:cq.Workplane|None = None
        self.ladders:cq.Workplane|None  = None
        self.cut_ring:cq.Workplane|None  = None

    def __make_ring(self):
        ring = shape.cone(
            radius=self.diameter/2,
            radius_top=self.diameter/2-self.inset,
            height=self.height
        )

        cut_ring = (
            cq.Workplane("XY")
            .cylinder(self.ladder_height, self.cut_diameter/2)
        )

        ring_slice = (cq.Workplane("XY").box(10,.5,self.height))

        self.cut_ring = cut_ring.translate((0,0,self.ladder_height/2))
        self.ring = (
            ring.cut(cut_ring)
            .translate((0,0,self.height/2))
            .cut(ring_slice.translate((self.diameter/2-.1,0,self.height/2)))
        )

    def __make_cut_ladders(self):
        x_translate = self.cut_diameter/2+self.ladder_length/2+self.ladder_cut_padding
        cut_ladder = (
            cq.Workplane("XY")
            .box(self.ladder_length,self.ladder_length,self.height)
            .faces("X or -X")
            .edges("Z")
            .chamfer(self.ladder_cut_chamfer)
            .translate((
                0,
                x_translate,
                self.height/2
            ))
        )

        cut_ladders = (
            cq.Workplane("XY")
            .union(cut_ladder)
            .union(cut_ladder.rotate((0,0,1),(0,0,0),180))
        )
        self.cut_ladders = cut_ladders

    def _make_ladder(self):
        bp = Ladder()
        bp.length = self.ladder_length
        bp.width = self.ladder_width
        bp.height = self.ladder_height
        bp.make()

        if bp.rungs:
            bp.rungs = bp.rungs.translate((0,self.ladder_width/4,0))

        ladder = bp.build()
        ladder = ladder.translate((
            0,
            self.cut_diameter/2+.6,
            self.ladder_height/2
        ))

        if self.cut_ring:
            ladder = ladder.cut(self.cut_ring)

        ladders = (
            cq.Workplane()
            .union(ladder)
            .union(ladder.rotate((0,0,1),(0,0,0),180))
        )

        self.ladders = ladders

    def make(self, parent = None):
        super().make(parent)
        self.__make_ring()

        if self.render_ladders:
            self.__make_cut_ladders()
            self._make_ladder()

    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.ring)
        )

        if self.render_ladders and self.ladders and self.cut_ladders:
            scene = (
                scene
                .cut(self.cut_ladders)
                .union(self.ladders)
            )
        return scene
