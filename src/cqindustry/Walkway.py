import cadquery as cq
from cadqueryhelper import Base, series, grid, irregular_grid, shape
import math

class Walkway(Base):
    def __init__(self):
        super().__init__()
        self.length = 75
        self.width = 50
        self.height = 5

        self.walkway_chamfer = 3

        self.render_slots = True # grid, irregular
        self.slot_length = 3
        self.slot_width_padding = 2
        self.slot_length_offset = 2
        self.slots_end_margin = 10

        ## regular tiles
        self.tile_length = 10
        self.tile_width = 10
        self.tile_height = 2
        self.tile_padding = 1
        self.make_tile_method = None

        ## irregular tiles
        self.tile_max_height = self.height
        self.tile_max_columns = 5
        self.tile_max_rows = 5
        self.tile_union_grid = False
        self.tile_seed = 'test'
        self.grid_width_padding = 2

        self.render_tabs = True
        self.tab_length = 5
        self.tab_height = 1
        self.tab_width_padding = 0
        self.tab_chamfer = 4.5

        self.render_rails = True # True, 'left', right, False
        self.rail_height = 15
        self.rail_width = 4
        self.rail_chamfer = 5

        self.render_rail_slots = True
        self.rail_slot_length = 3
        self.rail_slot_top_padding = 2
        self.rail_slot_length_offset = 2
        self.rail_slots_end_margin = 10
        self.rail_slot_pointed_inner_height = 5
        self.rail_slot_type = "box" # box, archpointed, archround

        self.walkway = None

        self.slots = None
        self.grid = None
        self.irregular_grid = None

        self.tabs = None
        self.rails = None
        self.rail_slots = None

    def __make_walkway(self):
        walkway = (
            cq.Workplane("XY")
            .box(self.length, self.width, self.height)
        )

        if self.walkway_chamfer:
            if self.walkway_chamfer < self.height:
                walkway = (
                    walkway
                    .faces("-Z")
                    .edges("not Y")
                    .chamfer(self.walkway_chamfer)
                )
            else:
                raise Exception(f"walkway_chamfer {self.walkway_chamfer} is too big for height {self.height}")


        self.walkway = walkway

    def __make_slots(self):
        slot_width = self.width - (self.slot_width_padding * 2 + self.rail_width * 2)
        slot = (
            cq.Workplane("XY")
            .slot2D(slot_width, self.slot_length)
            .extrude(self.height)
            .translate((0,0,-1*(self.height/2)))
            .rotate((0,0,1),(0,0,0),90)
        )

        size_length = self.length - self.slots_end_margin*2
        size = math.floor(size_length / (self.slot_length+self.slot_length_offset))

        slots = series(
            slot,
            length_offset = self.slot_length_offset,
            size = size
        )

        self.slots = slots

    def __make_grid(self):
        #self.grid = cq.Workplane("XY").box(20,20,20)
        tile = self.make_tile_method(
            self.tile_length - self.tile_padding,
            self.tile_width - self.tile_padding,
            self.tile_height
        )

        # this may be reverse
        rows = math.floor(self.length / self.tile_length)
        columns = math.floor((self.width - (self.grid_width_padding * 2 + self.rail_width * 2)) / self.tile_width)
        #print(f'columns {columns} rows {rows} length {self.length}, width {self.width}')
        #print(f'grid_width_padding {self.grid_width_padding*2} rail_width {self.rail_width*2}')


        tiles = grid.make_grid(
            part=tile,
            dim=[self.tile_length, self.tile_width],
            columns = columns,
            rows = rows
        )

        z_translate = self.height/2 + self.tile_height/2
        self.grid = tiles.translate((0,0,z_translate))

    def __make_irregular_grid(self):
        igrid = irregular_grid(
            length=self.length,
            width = self.width - (self.rail_width *2) - self.grid_width_padding,
            height = self.tile_height,
            make_item = self.make_tile_method,
            max_height = self.tile_max_height,
            max_columns = self.tile_max_columns,
            max_rows = self.tile_max_rows,
            union_grid = self.tile_union_grid,
            seed = self.tile_seed
        )
        self.irregular_grid = igrid.translate((0,0,self.height/2))

    def __make_tabs(self):
        x_translate = -1*(self.length/2+self.tab_length/2)
        z_translate = self.height/2-self.tab_height/2
        tab = (
            cq.Workplane("XY")
            .box(self.tab_length, self.width, self.tab_height)
            .translate((x_translate,0,z_translate))
            .faces("-X")
            .edges("Z")
            .chamfer(self.tab_chamfer)
        )

        tabs = (
            cq.Workplane("XY")
            .union(tab)
            .union(tab.rotate((0,0,1),(0,0,0),180))
        )
        self.tabs = tabs

    def __make_rails(self):
        y_translate = -1*(self.width/2-self.rail_width/2)
        z_translate = self.height/2+self.rail_height/2
        rail = (
            cq.Workplane("XY")
            .box(self.length, self.rail_width, self.rail_height)
            .translate((0,y_translate,z_translate))
        )

        if self.rail_chamfer:
            if self.rail_chamfer < self.rail_height:
                rail = (
                    rail
                    .faces("Z")
                    .edges("not X")
                    .chamfer(self.rail_chamfer)
                )
            else:
                raise Exception(f"rail_chamfer {self.rail_chamfer} is too big for rail_height {self.rail_height}")

        if self.render_rails == True:
            rails = (
                cq.Workplane("XY")
                .union(rail)
                .union(rail.rotate((0,0,1),(0,0,0),180))
            )
        elif self.render_rails == 'left':
            rails = (
                cq.Workplane("XY")
                #.union(rail)
                .union(rail.rotate((0,0,1),(0,0,0),180))
            )
        elif self.render_rails == 'right':
            rails = (
                cq.Workplane("XY")
                .union(rail)
                #.union(rail.rotate((0,0,1),(0,0,0),180))
            )

        self.rails = rails

    def __make_rail_slots(self):
        y_translate = -1*(self.width/2-self.rail_width/2)
        z_translate = self.height/2+self.rail_height/2
        slot_height = self.rail_height - self.rail_slot_top_padding

        # todo should lowercase
        slot_type = self.rail_slot_type.lower()
        if slot_type == "box":
            rail_slot = (
                cq.Workplane("XY")
                .box(self.rail_slot_length, self.rail_width, slot_height)
                .translate((0,0,-1*(self.rail_slot_top_padding/2)))
                .translate((0,y_translate,z_translate))
            )
        elif slot_type == 'archpointed':
            rail_slot = (
                shape.arch_pointed(
                  length=self.rail_slot_length,
                  width=self.rail_width,
                  height=slot_height,
                  inner_height=slot_height-self.rail_slot_pointed_inner_height
                )
                .translate((0,0,-1*(self.rail_slot_top_padding/2)))
                .translate((0,y_translate,z_translate))
            )
        elif slot_type == 'archround':
            rail_slot = (
                shape.arch_round(
                  length=self.rail_slot_length,
                  width=self.rail_width,
                  height=slot_height,
                )
                .translate((0,0,-1*(self.rail_slot_top_padding/2)))
                .translate((0,y_translate,z_translate))
            )
        else:
            raise Exception(f"Unrecognized rail_slot_type {slot_type}")

        size_length = self.length - self.rail_slots_end_margin*2
        size = math.floor(size_length / (self.rail_slot_length+self.rail_slot_length_offset))

        rail_slots = series(
            rail_slot,
            length_offset = self.rail_slot_length_offset,
            size = size
        )

        rail_slots_group = (
            cq.Workplane("XY")
            .union(rail_slots)
            .union(rail_slots.rotate((0,0,1),(0,0,0),180))
        )
        self.rail_slots = rail_slots_group

    def make(self):
        super().make()
        self.__make_walkway()

        if self.render_slots == True:
            self.__make_slots()
        elif self.render_slots == 'grid':
            self.__make_grid()
        elif self.render_slots == 'irregular':
            self.__make_irregular_grid()

        if self.render_tabs:
            self.__make_tabs()

        if self.render_rails:
            self.__make_rails()

        if self.render_rail_slots:
            self.__make_rail_slots()

    def build(self):
        super().build()
        scene = (
            cq.Workplane("XY")
            .union(self.walkway)
        )

        if self.render_slots and self.slots:
            scene = scene.cut(self.slots)
        elif self.render_slots == 'grid' and self.grid:
            scene = scene.union(self.grid)
        elif self.render_slots == 'irregular' and self.irregular_grid:
            scene = scene.union(self.irregular_grid)

        if self.render_tabs and self.tabs:
            scene = scene.union(self.tabs)

        if self.render_rails and self.rails:
            scene = scene.union(self.rails)

        if self.render_rail_slots and self.rail_slots:
            scene = scene.cut(self.rail_slots)
        return scene
