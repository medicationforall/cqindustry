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
from cadqueryhelper.grid import series, make_grid
import math

class Platform(Base):
    def __init__(self):
        super().__init__()
        self.length:float = 150
        self.width:float = 150
        self.height:float = 5
        self.corner_chamfer:float = 10

        self.render_center_cut:bool = True
        self.cut_diameter:float = 76

        self.render_stripes:bool = True
        self.stripe_width:float = 5
        self.stripe_side_padding:float = 3
        self.stripe_padding:float = .3

        self.bar_width:float = 5
        self.bar_inset:float = 1.5
        self.bar_padding:float = 1

        self.render_floor:bool = True
        self.floor_height:float = 1
        self.floor_tile_size:float = 12
        self.floor_tile_padding:float = 2
        self.floor_pading:float = 2

        self.render_ladders:bool = True
        self.ladder_length:float = 25
        self.ladder_width:float|None = None
        self.ladder_cut_chamfer:float = 2

        # parts
        self.center_cut = None
        self.platform = None
        self.stripe_cuts = None
        self.caution_stripes = None
        self.floor_tiles = None
        self.ladder_cuts = None

    def __make_platform(self):

        if self.corner_chamfer:
            platform = (
                cq.Workplane("XY")
                .box(self.length, self.width, self.height)
                .faces("X or -X")
                .edges("Z")
                .chamfer(self.corner_chamfer)
            )
        else:
            platform = cq.Workplane("XY").box(self.length, self.width, self.height)

        self.platform = platform

    def __make_center_cut(self):
        center_cut = (
            cq.Workplane("XY")
            .cylinder(self.height,(self.cut_diameter /2))
        )

        self.center_cut = center_cut

    def __make_stripe_cuts(self):
        stripe_y_length:float = self.length - self.corner_chamfer*2 - self.stripe_side_padding*2
        stripe_cut_y = (
            cq.Workplane("XY")
            .box(stripe_y_length, self.stripe_width, self.height)
            .translate((0,self.width/2-self.stripe_width/2,0))
        )

        stripe_x_length:float = self.width - self.corner_chamfer*2 - self.stripe_side_padding*2
        stripe_cut_x = (
            cq.Workplane("XY")
            .box(self.stripe_width, stripe_x_length, self.height)
            .translate((self.length/2-self.stripe_width/2,0,0))
        )

        stripes = (
            cq.Workplane("XY")
            .union(stripe_cut_y)
            .union(stripe_cut_y.rotate((0,0,1),(0,0,0),180))
            .union(stripe_cut_x)
            .union(stripe_cut_x.rotate((0,0,1),(0,0,0),180))
        )

        self.stripe_cuts = stripes


    def __caution_stripes(self):
        stripe_y_length:float = self.length - self.corner_chamfer*2 - self.stripe_side_padding*2
        stripe_x_length:float = self.width - self.corner_chamfer*2 - self.stripe_side_padding*2

        stripe_width:float = self.stripe_width - self.stripe_padding*2

        bar = (
            shape.rail(self.stripe_width, self.height, self.bar_width, self.bar_width-self.bar_inset)
            .rotate((1,0,0),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),90)
        )

        bar_space = self.bar_width+self.bar_padding*2
        size_y:float = math.floor(stripe_y_length/bar_space)
        size_x:float = math.floor(stripe_x_length/bar_space)

        bars_y:cq.Workplane = series(bar, length_offset=self.bar_padding*2, size=size_y)
        bars_x:cq.Workplane = series(bar, length_offset=self.bar_padding*2, size=size_x)

        stripe_y = (
            cq.Workplane("XY")
            .box(stripe_y_length, stripe_width, self.height-self.stripe_padding*4)
            .union(bars_y.translate((0,self.stripe_padding,0)))
            .translate((0,self.width/2-stripe_width/2-self.stripe_padding*2,0))
        )

        stripe_x = (
            cq.Workplane("XY")
            .box(stripe_width, stripe_x_length, self.height-self.stripe_padding*4)
            .union(bars_x.rotate((0,0,9),(0,0,0),-90).translate((self.stripe_padding,0,0)))
            .translate((self.length/2-stripe_width/2-self.stripe_padding*2,0,0))
        )

        stripes = (
            cq.Workplane("XY")
            .union(stripe_y)
            .union(stripe_y.rotate((0,0,1),(0,0,0),180))
            .union(stripe_x)
            .union(stripe_x.rotate((0,0,1),(0,0,0),180))
        )

        self.caution_stripes = stripes

    def __make_floor_tiles(self):
        diamond:cq.Workplane = shape.diamond(
            self.floor_tile_size,
            self.floor_tile_size,
            self.floor_height
        ).faces("-Z").chamfer(.4)


        rows:int = math.floor((self.length-self.height) / (self.floor_tile_size+self.floor_tile_padding))
        colums:int = math.floor((self.width-self.height) / ((self.floor_tile_size+self.floor_tile_padding)/2))

        diamonds:cq.Workplane = make_grid(
            diamond,
            [self.floor_tile_size+self.floor_tile_padding, (self.floor_tile_size+self.floor_tile_padding)/2],
            rows = rows+2,
            columns = colums+2,
            odd_col_push = [(self.floor_tile_size+self.floor_tile_padding)/2,0]
        )

        if self.corner_chamfer:
            outline = (
                cq.Workplane("XY")
                .box(
                    self.length-(self.stripe_width+self.floor_pading)*2,
                    self.width-(self.stripe_width+self.floor_pading)*2,
                    self.height/2
                )
                .faces("X or -X")
                .edges("Z")
                .chamfer(self.corner_chamfer)
                .translate((0,0,self.height/2))
            )
        else:
            outline = (
                cq.Workplane("XY")
                .box(
                    self.length-(self.stripe_width+self.floor_pading)*2,
                    self.width-(self.stripe_width+self.floor_pading)*2,
                    self.height/2
                )
                .translate((0,0,self.height/2))
            )

        floor_tiles:cq.Workplane = diamonds.translate((
            0,
            0,
            self.floor_height/2+self.height/2
        ))
        #self.floor_tiles = outline
        self.floor_tiles = outline.intersect(floor_tiles).translate((0,0,-1))

    def __make_ladder_cuts(self):
        ladder_width = self.ladder_length

        if self.ladder_width:
            ladder_width = self.ladder_width

        ladder_cut = (
            cq.Workplane("XY")
            .box(
                self.ladder_length,
                ladder_width,
                self.height
            )
            .faces("X or -X")
            .edges("Z")
            .chamfer(self.ladder_cut_chamfer)
            .translate((
                0,
                self.cut_diameter/2+ladder_width/2-4,
                0
            ))
        )

        ladder_cuts = (
            cq.Workplane("XY")
            .union(ladder_cut.rotate((0,0,1),(0,0,0),45))
            .union(ladder_cut.rotate((0,0,1),(0,0,0),225))
        )
        self.ladder_cuts = ladder_cuts

    def make(self, parent = None):
        super().make(parent)
        self.__make_platform()

        #if self.render_center_cut:
        self.__make_center_cut()

        if self.render_floor:
            self.__make_floor_tiles()

        #if self.render_ladders:
        self.__make_ladder_cuts()

        if self.render_stripes:
            self.__make_stripe_cuts()
            self.__caution_stripes()

    def build(self) -> cq.Workplane:
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.platform)
        )

        if self.render_center_cut and self.center_cut:
            scene = scene.cut(self.center_cut)

        if self.render_floor and self.floor_tiles:
            scene = scene.cut(self.floor_tiles)

        if self.render_ladders and self.ladder_cuts:
            scene = scene.cut(self.ladder_cuts)

        if self.render_stripes:
            if self.stripe_cuts:
                scene = scene.cut(self.stripe_cuts)

            if self.caution_stripes:
                scene = scene.union(self.caution_stripes)

        return scene
