import cadquery as cq
from cqindustry.barricade import Wall

from cqindustry.barricade.tiles import (
    plain,
    slot,
    rivet,
    vent,
    bolt_panel,
    corrugated,
    charge
)

bp_wall = Wall()

bp_wall.length:float = 75
bp_wall.width:float = 25
bp_wall.height:float = 60

bp_wall.seed = 'flay'
bp_wall.base_height = 3
bp_wall.vertical_beam_count = 2
bp_wall.verical_beam_width = 5

bp_wall.beam_length = 25
bp_wall.beam_height = 10
bp_wall.web_thickness = 2
bp_wall.length_inset = 15

bp_wall.tiles= [
    bolt_panel,
    bolt_panel,
    charge,
    rivet,
    rivet,
    slot,
    slot,
    vent, 
    corrugated,
    corrugated
]

bp_wall.render_grid = True
bp_wall.grid_x_spacing = 5
bp_wall.grid_y_spacing = 5
bp_wall.grid_x_stretch = (1,4,1)
bp_wall.grid_y_stretch = (1,3,1)
bp_wall.grid_height = (2,3,1)

bp_wall.h_bleam_width = 5
bp_wall.h_beam_height= 10

bp_wall.render_panels = True
bp_wall.panel_width = 10
bp_wall.panel_count = (2,4,1)
bp_wall.panel_rotate = (-45,60,5)
bp_wall.panel_tiles = [rivet,bolt_panel]
#bp_wall.panel_seed = 'test'

bp_wall.make()

ex_wall = bp_wall.build()

#show_object(ex_wall)
cq.exporters.export(ex_wall,'stl/barricade_wall.stl')