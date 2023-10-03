import cadquery as cq
from . import Base
from cadqueryhelper import shape, series, grid
import math

class Platform(Base):
    def __init__(self):
        super().__init__()
        self.length = 150
        self.width = 150
        self.height = 5
        self.corner_chamfer = 10

        self.render_center_cut = True
        self.cut_diameter = 76

        self.render_stripes = True
        self.stripe_width = 5
        self.stripe_side_padding = 3
        self.stripe_padding = .3

        self.bar_width = 5
        self.bar_inset = 1.5
        self.bar_padding = 1

        self.render_floor = True
        self.floor_height = 1
        self.floor_tile_size = 12
        self.floor_tile_padding = 2
        self.floor_pading =2

        self.render_ladders = True
        self.ladder_length = 25
        self.ladder_cut_chamfer = 2

        # parts
        self.center_cut = None
        self.platform = None
        self.stripe_cuts = None
        self.caution_stripes = None
        self.floor_tiles = None
        self.ladder_cuts = None

    def __make_platform(self):
        platform = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height)
            .faces("X or -X")
            .edges("Z")
            .chamfer(self.corner_chamfer)
        )

        self.platform = platform

    def __make_center_cut(self):
        center_cut = (
            cq.Workplane("XY")
            .cylinder(self.height,(self.cut_diameter /2))
        )

        self.center_cut = center_cut

    def __make_stripe_cuts(self):
        stripe_y_length = self.length - self.corner_chamfer*2 - self.stripe_side_padding*2
        stripe_cut_y = (
            cq.Workplane("XY")
            .box(stripe_y_length, self.stripe_width, self.height)
            .translate((0,self.width/2-self.stripe_width/2,0))
        )

        stripe_x_length = self.width - self.corner_chamfer*2 - self.stripe_side_padding*2
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
        stripe_y_length = self.length - self.corner_chamfer*2 - self.stripe_side_padding*2
        stripe_x_length = self.width - self.corner_chamfer*2 - self.stripe_side_padding*2

        stripe_width = self.stripe_width - self.stripe_padding*2

        bar = (
            shape.rail(self.stripe_width, self.height, self.bar_width, self.bar_width-self.bar_inset)
            .rotate((1,0,0),(0,0,0),90)
            .rotate((0,0,1),(0,0,0),90)
        )

        bar_space = self.bar_width+self.bar_padding*2
        size_y = math.floor(stripe_y_length/bar_space)
        size_x = math.floor(stripe_x_length/bar_space)

        bars_y = series(bar, length_offset=self.bar_padding*2, size=size_y)
        bars_x = series(bar, length_offset=self.bar_padding*2, size=size_x)

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
        diamond = shape.diamond(
            self.floor_tile_size,
            self.floor_tile_size,
            self.floor_height
        ).faces("-Z").chamfer(.4)


        rows = math.floor((self.length-self.height) / (self.floor_tile_size+self.floor_tile_padding))
        colums = math.floor((self.width-self.height) / ((self.floor_tile_size+self.floor_tile_padding)/2))

        diamonds = grid.make_grid(
            diamond,
            [self.floor_tile_size+self.floor_tile_padding, (self.floor_tile_size+self.floor_tile_padding)/2],
            rows = rows+2,
            columns = colums+2,
            odd_col_push = [(self.floor_tile_size+self.floor_tile_padding)/2,0]
        )

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

        floor_tiles = diamonds.translate((
            0,
            0,
            self.floor_height/2+self.height/2
        ))
        #self.floor_tiles = outline
        self.floor_tiles = outline.intersect(floor_tiles).translate((0,0,-1))

    def __make_ladder_cuts(self):
        ladder_cut = (
            cq.Workplane("XY")
            .box(
                self.ladder_length,
                self.ladder_length,
                self.height
            )
            .faces("X or -X")
            .edges("Z")
            .chamfer(self.ladder_cut_chamfer)
            .translate((
                0,
                self.cut_diameter/2+self.ladder_length/2-4,
                0
            ))
        )

        ladder_cuts = (
            cq.Workplane("XY")
            .union(ladder_cut.rotate((0,0,1),(0,0,0),45))
            .union(ladder_cut.rotate((0,0,1),(0,0,0),225))
        )
        self.ladder_cuts = ladder_cuts

    def make(self):
        super().make()
        self.__make_platform()

        if self.render_center_cut:
            self.__make_center_cut()

        if self.render_floor:
            self.__make_floor_tiles()

        if self.render_ladders:
            self.__make_ladder_cuts()

        if self.render_stripes:
            self.__make_stripe_cuts()
            self.__caution_stripes()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.platform)
        )

        if self.render_center_cut and self.center_cut:
            scene = scene.cut(self.center_cut)

        if self.render_floor and self.floor_tiles:
            scene = scene.cut(self.floor_tiles)

        if self.render_ladders:
            scene = scene.cut(self.ladder_cuts)

        if self.render_stripes:
            if self.stripe_cuts:
                scene = scene.cut(self.stripe_cuts)

            if self.caution_stripes:
                scene.add(self.caution_stripes)

        return scene
