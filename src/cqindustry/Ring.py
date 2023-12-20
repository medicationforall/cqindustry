import cadquery as cq
from cadqueryhelper import Base, shape
from cqterrain import Ladder

class Ring(Base):
    def __init__(self):
        super().__init__()
        self.cut_diameter = 76
        self.diameter = self.cut_diameter + 10
        self.inset = 5
        self.height = 10

        self.render_ladders = True
        self.ladder_height = 71
        self.ladder_length = 25
        self.ladder_width = 10
        self.ladder_cut_padding = 1.5
        self.ladder_cut_chamfer = 2

        self.ring = None
        self.cut_ladders = None
        self.ladders = None
        self.cut_ring = None

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

    def __make_ladder(self):
        bp = Ladder()
        bp.length = self.ladder_length
        bp.width = self.ladder_width
        bp.height = self.ladder_height
        bp.make()
        bp.rungs = bp.rungs.translate((0,self.ladder_width/4,0))

        ladder = bp.build()

        ladder = ladder.translate((
            0,
            self.cut_diameter/2+.6,
            self.ladder_height/2
        )).cut(self.cut_ring)

        ladders = (
            cq.Workplane()
            .union(ladder)
            .union(ladder.rotate((0,0,1),(0,0,0),180))
        )

        #show_object(ladders)

        self.ladders = ladders

    def make(self):
        super().make()
        self.__make_ring()

        if self.render_ladders:
            self.__make_cut_ladders()
            self.__make_ladder()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.ring)
        )

        if self.render_ladders and self.ladders:
            scene = (
                scene
                .cut(self.cut_ladders)
                .union(self.ladders)
            )
        return scene
